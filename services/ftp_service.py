"""
FTP 서비스 모듈 - FTP 업데이트 관련 기능
"""

from PyQt5.QtCore import QThread, pyqtSignal
import ftplib
import tempfile
from config.ftp_config import FTPConfig


class FTPUpdateChecker(QThread):
    """FTP 서버에서 업데이트 확인을 위한 스레드"""
    
    update_available = pyqtSignal(str, str, str)
    check_completed = pyqtSignal(bool)
    
    def __init__(self):
        """FTPUpdateChecker 초기화"""
        super().__init__()
        self.ftp_host, self.ftp_user, self.ftp_pass = FTPConfig.get_connection_info()
        
    def run(self):
        """업데이트 확인 실행"""
        try:
            ftp = ftplib.FTP(self.ftp_host)
            ftp.login(self.ftp_user, self.ftp_pass)
            
            version_file = FTPConfig.get_version_file_path()
            changelog_file = FTPConfig.get_changelog_file_path()
            
            with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_version:
                ftp.retrbinary(f'RETR {version_file}', temp_version.write)
                temp_version.seek(0)
                latest_version = temp_version.read().strip()
            
            with tempfile.NamedTemporaryFile(mode='w+', delete=False) as temp_changelog:
                ftp.retrbinary(f'RETR {changelog_file}', temp_changelog.write)
                temp_changelog.seek(0)
                changelog = temp_changelog.read()
            
            current_version = "1.0.0"
            
            if self.is_newer_version(latest_version):
                filename = f"RPA_Smart_Key-in_Manager_{latest_version}.exe"
                self.update_available.emit(latest_version, filename, changelog)
                self.check_completed.emit(True)
            else:
                self.check_completed.emit(False)
                
            ftp.quit()
            
        except Exception as e:
            print(f"업데이트 확인 중 오류: {e}")
            self.check_completed.emit(False)
    
    def is_newer_version(self, latest_version):
        """
        최신 버전인지 확인
        
        Args:
            latest_version (str): 최신 버전 문자열
            
        Returns:
            bool: 최신 버전 여부
        """
        current_version = "1.0.0"
        return self.is_version_greater(latest_version, current_version)
    
    def is_version_greater(self, version1, version2):
        """
        버전 비교
        
        Args:
            version1 (str): 비교할 버전1
            version2 (str): 비교할 버전2
            
        Returns:
            bool: version1이 version2보다 큰지 여부
        """
        def version_to_tuple(version):
            return tuple(map(int, version.split('.')))
        
        return version_to_tuple(version1) > version_to_tuple(version2)


class FTPUpdateDownloader(QThread):
    """FTP 서버에서 파일 다운로드를 위한 스레드"""
    
    progress_updated = pyqtSignal(int)
    download_finished = pyqtSignal(str)
    download_failed = pyqtSignal(str)
    
    def __init__(self, filename):
        """
        FTPUpdateDownloader 초기화
        
        Args:
            filename (str): 다운로드할 파일명
        """
        super().__init__()
        self.filename = filename
        self.ftp_host, self.ftp_user, self.ftp_pass = FTPConfig.get_connection_info()
        
    def run(self):
        """파일 다운로드 실행"""
        try:
            ftp = ftplib.FTP(self.ftp_host)
            ftp.login(self.ftp_user, self.ftp_pass)
            
            file_size = ftp.size(self.filename)
            
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.exe')
            downloaded = 0
            
            def handle_binary(data):
                nonlocal downloaded
                temp_file.write(data)
                downloaded += len(data)
                if file_size > 0:
                    progress = int((downloaded / file_size) * 100)
                    self.progress_updated.emit(progress)
            
            ftp.retrbinary(f'RETR {self.filename}', handle_binary)
            temp_file.close()
            ftp.quit()
            
            self.download_finished.emit(temp_file.name)
            
        except Exception as e:
            error_msg = f"다운로드 중 오류 발생: {e}"
            print(error_msg)
            self.download_failed.emit(error_msg)