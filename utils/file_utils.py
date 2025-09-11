"""
파일 처리 유틸리티 모듈
"""

import os
import tempfile
import shutil
import hashlib
from datetime import datetime


class FileUtils:
    """파일 처리 관련 유틸리티 클래스"""
    
    @staticmethod
    def ensure_directory_exists(directory_path):
        """
        디렉토리가 존재하지 않으면 생성
        
        Args:
            directory_path (str): 디렉토리 경로
            
        Returns:
            bool: 생성 성공 여부
        """
        try:
            os.makedirs(directory_path, exist_ok=True)
            return True
        except Exception as e:
            print(f"디렉토리 생성 실패: {e}")
            return False
    
    @staticmethod
    def copy_file_with_backup(source_path, destination_path, backup_suffix='.backup'):
        """
        파일 복사 시 기존 파일을 백업
        
        Args:
            source_path (str): 원본 파일 경로
            destination_path (str): 대상 파일 경로
            backup_suffix (str): 백업 파일 접미사
            
        Returns:
            bool: 복사 성공 여부
        """
        try:
            if os.path.exists(destination_path):
                backup_path = destination_path + backup_suffix
                shutil.copy2(destination_path, backup_path)
                print(f"기존 파일 백업: {backup_path}")
            
            shutil.copy2(source_path, destination_path)
            print(f"파일 복사 완료: {source_path} -> {destination_path}")
            return True
            
        except Exception as e:
            print(f"파일 복사 실패: {e}")
            return False
    
    @staticmethod
    def get_file_hash(file_path, algorithm='md5'):
        """
        파일의 해시값 계산
        
        Args:
            file_path (str): 파일 경로
            algorithm (str): 해시 알고리즘 ('md5', 'sha1', 'sha256')
            
        Returns:
            str: 파일 해시값 (오류 시 None)
        """
        try:
            hash_func = hashlib.new(algorithm)
            
            with open(file_path, 'rb') as f:
                for chunk in iter(lambda: f.read(4096), b""):
                    hash_func.update(chunk)
            
            return hash_func.hexdigest()
            
        except Exception as e:
            print(f"파일 해시 계산 실패: {e}")
            return None
    
    @staticmethod
    def get_file_info(file_path):
        """
        파일 정보 반환
        
        Args:
            file_path (str): 파일 경로
            
        Returns:
            dict: 파일 정보 딕셔너리
        """
        try:
            stat = os.stat(file_path)
            
            return {
                'name': os.path.basename(file_path),
                'path': file_path,
                'size': stat.st_size,
                'size_mb': round(stat.st_size / (1024 * 1024), 2),
                'created': datetime.fromtimestamp(stat.st_ctime),
                'modified': datetime.fromtimestamp(stat.st_mtime),
                'accessed': datetime.fromtimestamp(stat.st_atime),
                'is_file': os.path.isfile(file_path),
                'is_dir': os.path.isdir(file_path),
                'exists': os.path.exists(file_path)
            }
            
        except Exception as e:
            print(f"파일 정보 조회 실패: {e}")
            return None
    
    @staticmethod
    def clean_temp_files(pattern_prefix='RPA_Smart_Key-in', max_age_hours=24):
        """
        임시 파일 정리
        
        Args:
            pattern_prefix (str): 파일명 패턴 접두사
            max_age_hours (int): 최대 보존 시간 (시간)
            
        Returns:
            int: 삭제된 파일 수
        """
        deleted_count = 0
        try:
            temp_dir = tempfile.gettempdir()
            current_time = datetime.now()
            
            for filename in os.listdir(temp_dir):
                if filename.startswith(pattern_prefix):
                    file_path = os.path.join(temp_dir, filename)
                    
                    try:
                        file_time = datetime.fromtimestamp(os.path.getmtime(file_path))
                        age_hours = (current_time - file_time).total_seconds() / 3600
                        
                        if age_hours > max_age_hours:
                            os.remove(file_path)
                            deleted_count += 1
                            print(f"임시 파일 삭제: {file_path}")
                            
                    except Exception as e:
                        print(f"파일 삭제 실패 {file_path}: {e}")
            
            return deleted_count
            
        except Exception as e:
            print(f"임시 파일 정리 중 오류: {e}")
            return 0
    
    @staticmethod
    def safe_file_write(file_path, content, mode='w', encoding='utf-8'):
        """
        안전한 파일 쓰기 (임시 파일 사용 후 원자적 이동)
        
        Args:
            file_path (str): 대상 파일 경로
            content (str): 파일 내용
            mode (str): 파일 쓰기 모드
            encoding (str): 인코딩
            
        Returns:
            bool: 쓰기 성공 여부
        """
        try:
            directory = os.path.dirname(file_path)
            FileUtils.ensure_directory_exists(directory)
            
            with tempfile.NamedTemporaryFile(mode=mode, encoding=encoding, 
                                           dir=directory, delete=False) as temp_file:
                temp_file.write(content)
                temp_path = temp_file.name
            
            shutil.move(temp_path, file_path)
            print(f"파일 쓰기 완료: {file_path}")
            return True
            
        except Exception as e:
            print(f"파일 쓰기 실패: {e}")
            try:
                if 'temp_path' in locals() and os.path.exists(temp_path):
                    os.remove(temp_path)
            except:
                pass
            return False
    
    @staticmethod
    def get_available_filename(base_path):
        """
        사용 가능한 파일명 반환 (중복 시 번호 추가)
        
        Args:
            base_path (str): 기본 파일 경로
            
        Returns:
            str: 사용 가능한 파일 경로
        """
        if not os.path.exists(base_path):
            return base_path
        
        directory = os.path.dirname(base_path)
        filename = os.path.basename(base_path)
        name, ext = os.path.splitext(filename)
        
        counter = 1
        while True:
            new_filename = f"{name}_{counter}{ext}"
            new_path = os.path.join(directory, new_filename)
            
            if not os.path.exists(new_path):
                return new_path
            
            counter += 1