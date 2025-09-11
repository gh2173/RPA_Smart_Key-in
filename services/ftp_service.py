"""
FTP 서비스 모듈 - FTP 업데이트 관련 기능
"""

from PyQt5.QtCore import QThread, pyqtSignal
import ftplib
import tempfile
import os
import re


class FTPUpdateChecker(QThread):
    """FTP 서버에서 업데이트 확인을 위한 스레드"""
    
    update_available = pyqtSignal(str, str, str)  # 버전, 파일명, 변경사항
    check_completed = pyqtSignal(bool)  # 확인 완료 여부
    
    def __init__(self):
        super().__init__()
        self.current_version = "4.1.1"  # 현재 프로그램 버전
        self.ftp_host = "192.168.223.225"
        self.ftp_user = "vega"
        self.ftp_pass = "vegagcc"
        self.ftp_path = "/"
    
    def run(self):
        print(f"현재 설정된 버전: {self.current_version}")
        try:
            # FTP 연결
            ftp = ftplib.FTP(self.ftp_host)
            ftp.login(self.ftp_user, self.ftp_pass)
            
            # 경로가 루트가 아니면 해당 디렉토리로 이동
            if self.ftp_path != "/":
                try:
                    ftp.cwd(self.ftp_path)
                except ftplib.error_perm as e:
                    print(f"FTP 경로 '{self.ftp_path}' 이동 실패: {e}")
                    print("루트 디렉토리에서 파일을 검색합니다.")
            
            # 디렉토리 파일 목록 가져오기
            files = []
            ftp.retrlines('LIST', files.append)
            
            # RPA Smart Key-in 실행 파일 찾기 (패턴: RPA_Smart_Key-in_X.X.X.exe)
            exe_pattern = r'(?:RPA_Smart_Key-in_)?(\d+\.\d+\.\d+)\.exe'
            latest_version = None
            latest_filename = None
            
            print(f"FTP 서버 파일 목록 확인 중... (총 {len(files)}개 파일)")
            
            for file_line in files:
                # LIST 결과에서 파일명 추출
                filename = file_line.split()[-1]
                print(f"검사 중인 파일: {filename}")
                
                match = re.search(exe_pattern, filename)
                if match:
                    version = match.group(1)
                    print(f"업데이트 파일 발견: {filename} (버전: {version})")
                    
                    print(f"버전 비교: {version} vs {self.current_version}")
                    print(f"is_newer_version 결과: {self.is_newer_version(version)}")
                    if self.is_newer_version(version):
                        if latest_version is None or self.is_version_greater(version, latest_version):
                            latest_version = version
                            latest_filename = filename
                            print(f"새로운 최신 버전으로 설정: {version}")
                    else:
                        print(f"버전 {version}은 현재 버전 {self.current_version}보다 낮거나 같음")
            
            if latest_version and latest_filename:
                # version.txt가 있는지 확인해서 변경사항 가져오기 (선택사항)
                changelog = "업데이트 내용 없음"
                try:
                    version_data = []
                    ftp.retrlines('RETR version.txt', version_data.append)
                    if len(version_data) > 3:
                        changelog = '\n'.join(version_data[3:])
                except:
                    # version.txt가 없어도 괜찮음
                    pass
                
                self.update_available.emit(latest_version, latest_filename, changelog)
                self.check_completed.emit(True)
            else:
                self.check_completed.emit(False)
            
            ftp.quit()
                        
        except Exception as e:
            print(f"FTP 업데이트 확인 실패: {e}")
            print(f"FTP 서버: {self.ftp_host}")
            print(f"에러 타입: {type(e).__name__}")
            import traceback
            traceback.print_exc()
            self.check_completed.emit(False)
    
    def is_newer_version(self, latest_version):
        try:
            current = list(map(int, self.current_version.split('.')))
            latest = list(map(int, latest_version.split('.')))
            return latest > current
        except:
            return False
    
    def is_version_greater(self, version1, version2):
        try:
            v1 = list(map(int, version1.split('.')))
            v2 = list(map(int, version2.split('.')))
            return v1 > v2
        except:
            return False


class FTPUpdateDownloader(QThread):
    """FTP 서버에서 파일 다운로드를 위한 스레드"""
    
    progress_updated = pyqtSignal(int)
    download_finished = pyqtSignal(str)  # 다운로드된 파일 경로
    download_failed = pyqtSignal(str)    # 에러 메시지
    
    def __init__(self, filename):
        super().__init__()
        self.filename = filename
        self.ftp_host = "192.168.223.225"
        self.ftp_user = "vega"
        self.ftp_pass = "vegagcc"
        self.ftp_path = "/"
    
    def run(self):
        try:
            # FTP 연결
            ftp = ftplib.FTP(self.ftp_host)
            ftp.login(self.ftp_user, self.ftp_pass)
            
            # 경로가 루트가 아니면 해당 디렉토리로 이동
            if self.ftp_path != "/":
                try:
                    ftp.cwd(self.ftp_path)
                except ftplib.error_perm as e:
                    print(f"FTP 다운로드 경로 '{self.ftp_path}' 이동 실패: {e}")
                    self.download_failed.emit(f"FTP 경로 오류: {str(e)}")
                    return
            
            # 파일 크기 확인
            try:
                file_size = ftp.size(self.filename)
            except:
                file_size = 0
            
            # 임시 폴더에 다운로드
            temp_dir = tempfile.gettempdir()
            local_path = os.path.join(temp_dir, self.filename)
            
            downloaded = 0
            
            def handle_binary(data):
                nonlocal downloaded
                with open(local_path, 'ab') as f:
                    f.write(data)
                downloaded += len(data)
                if file_size > 0:
                    progress = int((downloaded / file_size) * 100)
                    self.progress_updated.emit(progress)
                else:
                    # 파일 크기를 모르는 경우 임의의 진행률 표시
                    progress = min(int(downloaded / (1024*1024) * 10), 90)  # 1MB당 10%
                    self.progress_updated.emit(progress)
            
            # 파일 다운로드
            with open(local_path, 'wb') as f:
                pass  # 파일 초기화
            
            ftp.retrbinary(f'RETR {self.filename}', handle_binary)
            ftp.quit()
            
            self.progress_updated.emit(100)
            self.download_finished.emit(local_path)
                        
        except Exception as e:
            self.download_failed.emit(str(e))