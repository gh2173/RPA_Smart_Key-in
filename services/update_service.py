"""
업데이트 서비스 모듈 - 애플리케이션 업데이트 관련 기능
"""

import subprocess
import tempfile
import os
from PyQt5.QtCore import QSettings


class UpdateService:
    """애플리케이션 업데이트 관리 서비스"""
    
    def __init__(self):
        """UpdateService 초기화"""
        self.settings = QSettings('NEPES', 'RPA_Smart_Key-in_Manager')
    
    def check_auto_update_enabled(self):
        """
        자동 업데이트 설정 확인
        
        Returns:
            bool: 자동 업데이트 활성화 여부
        """
        return self.settings.value('auto_update', True, type=bool)
    
    def set_auto_update_enabled(self, enabled):
        """
        자동 업데이트 설정
        
        Args:
            enabled (bool): 자동 업데이트 활성화 여부
        """
        self.settings.setValue('auto_update', enabled)
    
    def get_current_version(self):
        """
        현재 애플리케이션 버전 반환
        
        Returns:
            str: 현재 버전
        """
        return self.settings.value('version', '1.0.0', type=str)
    
    def set_current_version(self, version):
        """
        현재 애플리케이션 버전 설정
        
        Args:
            version (str): 설정할 버전
        """
        self.settings.setValue('version', version)
    
    def install_update(self, new_exe_path):
        """
        업데이트 설치
        
        Args:
            new_exe_path (str): 새 실행파일 경로
            
        Returns:
            bool: 설치 성공 여부
        """
        try:
            current_exe = os.path.abspath(__file__)
            backup_exe = current_exe + '.backup'
            
            if os.path.exists(backup_exe):
                os.remove(backup_exe)
            
            os.rename(current_exe, backup_exe)
            
            import shutil
            shutil.copy2(new_exe_path, current_exe)
            
            print("업데이트가 성공적으로 설치되었습니다.")
            return True
            
        except Exception as e:
            print(f"업데이트 설치 중 오류: {e}")
            
            try:
                if os.path.exists(backup_exe):
                    os.rename(backup_exe, current_exe)
                print("백업에서 복구되었습니다.")
            except:
                print("백업 복구에 실패했습니다.")
            
            return False
    
    def perform_update(self, new_exe_path):
        """
        업데이트 수행 (애플리케이션 재시작)
        
        Args:
            new_exe_path (str): 새 실행파일 경로
        """
        try:
            batch_script = self.create_update_batch_script(new_exe_path)
            subprocess.Popen([batch_script], shell=True)
            
        except Exception as e:
            print(f"업데이트 수행 중 오류: {e}")
    
    def create_update_batch_script(self, new_exe_path):
        """
        업데이트용 배치 스크립트 생성
        
        Args:
            new_exe_path (str): 새 실행파일 경로
            
        Returns:
            str: 배치 스크립트 경로
        """
        current_exe = os.path.abspath(__file__)
        
        batch_content = f"""
@echo off
timeout /t 3 /nobreak > nul
taskkill /f /im "{os.path.basename(current_exe)}" > nul 2>&1
timeout /t 2 /nobreak > nul
copy /y "{new_exe_path}" "{current_exe}"
if %errorlevel% == 0 (
    echo 업데이트가 완료되었습니다.
    start "" "{current_exe}"
) else (
    echo 업데이트에 실패했습니다.
    pause
)
del "{new_exe_path}"
del "%~f0"
"""
        
        with tempfile.NamedTemporaryFile(mode='w', suffix='.bat', delete=False) as batch_file:
            batch_file.write(batch_content)
            return batch_file.name
    
    def cleanup_temp_files(self):
        """임시 파일 정리"""
        try:
            temp_dir = tempfile.gettempdir()
            for filename in os.listdir(temp_dir):
                if filename.startswith('RPA_Smart_Key-in') and filename.endswith('.exe'):
                    temp_file_path = os.path.join(temp_dir, filename)
                    try:
                        os.remove(temp_file_path)
                        print(f"임시 파일 삭제: {temp_file_path}")
                    except:
                        pass
        except Exception as e:
            print(f"임시 파일 정리 중 오류: {e}")
    
    def verify_update_integrity(self, file_path):
        """
        업데이트 파일 무결성 검증
        
        Args:
            file_path (str): 검증할 파일 경로
            
        Returns:
            bool: 파일 무결성 여부
        """
        try:
            if not os.path.exists(file_path):
                return False
            
            file_size = os.path.getsize(file_path)
            if file_size < 1024:  # 1KB 미만이면 유효하지 않음
                return False
            
            with open(file_path, 'rb') as f:
                header = f.read(2)
                if header != b'MZ':  # Windows PE 파일 헤더 확인
                    return False
            
            return True
            
        except Exception as e:
            print(f"파일 무결성 검증 중 오류: {e}")
            return False