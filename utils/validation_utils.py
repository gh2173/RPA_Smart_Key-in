"""
검증 유틸리티 모듈
"""

import re
import socket
from datetime import datetime


class ValidationUtils:
    """데이터 검증 관련 유틸리티 클래스"""
    
    @staticmethod
    def is_valid_equipment_id(eqp_id):
        """
        장비 ID 유효성 검증
        
        Args:
            eqp_id (str): 장비 ID
            
        Returns:
            bool: 유효성 여부
        """
        if not eqp_id or not isinstance(eqp_id, str):
            return False
        
        eqp_id = eqp_id.strip()
        
        if len(eqp_id) < 3 or len(eqp_id) > 20:
            return False
        
        pattern = r'^[A-Z0-9_-]+$'
        return bool(re.match(pattern, eqp_id))
    
    @staticmethod
    def is_valid_user_id(user_id):
        """
        사용자 ID 유효성 검증
        
        Args:
            user_id (str): 사용자 ID
            
        Returns:
            bool: 유효성 여부
        """
        if not user_id or not isinstance(user_id, str):
            return False
        
        user_id = user_id.strip()
        
        if len(user_id) < 3 or len(user_id) > 15:
            return False
        
        pattern = r'^[a-zA-Z0-9_]+$'
        return bool(re.match(pattern, user_id))
    
    @staticmethod
    def is_valid_ip_address(ip_address):
        """
        IP 주소 유효성 검증
        
        Args:
            ip_address (str): IP 주소
            
        Returns:
            bool: 유효성 여부
        """
        try:
            socket.inet_aton(ip_address)
            return True
        except socket.error:
            return False
    
    @staticmethod
    def is_valid_port(port):
        """
        포트 번호 유효성 검증
        
        Args:
            port (int|str): 포트 번호
            
        Returns:
            bool: 유효성 여부
        """
        try:
            port_num = int(port)
            return 1 <= port_num <= 65535
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def is_valid_version(version):
        """
        버전 문자열 유효성 검증
        
        Args:
            version (str): 버전 문자열 (예: "1.0.0")
            
        Returns:
            bool: 유효성 여부
        """
        if not version or not isinstance(version, str):
            return False
        
        pattern = r'^\d+\.\d+\.\d+$'
        return bool(re.match(pattern, version.strip()))
    
    @staticmethod
    def is_valid_database_name(db_name):
        """
        데이터베이스명 유효성 검증
        
        Args:
            db_name (str): 데이터베이스명
            
        Returns:
            bool: 유효성 여부
        """
        if not db_name or not isinstance(db_name, str):
            return False
        
        db_name = db_name.strip()
        
        if len(db_name) < 1 or len(db_name) > 30:
            return False
        
        pattern = r'^[a-zA-Z0-9_]+$'
        return bool(re.match(pattern, db_name))
    
    @staticmethod
    def is_valid_file_path(file_path):
        """
        파일 경로 유효성 검증 (형식만 검증, 실제 존재 여부는 확인하지 않음)
        
        Args:
            file_path (str): 파일 경로
            
        Returns:
            bool: 유효성 여부
        """
        if not file_path or not isinstance(file_path, str):
            return False
        
        file_path = file_path.strip()
        
        if len(file_path) < 1:
            return False
        
        invalid_chars = '<>:"|?*'
        for char in invalid_chars:
            if char in file_path:
                return False
        
        return True
    
    @staticmethod
    def is_valid_datetime_string(datetime_str, format='%Y-%m-%d %H:%M:%S'):
        """
        날짜시간 문자열 유효성 검증
        
        Args:
            datetime_str (str): 날짜시간 문자열
            format (str): 날짜시간 형식
            
        Returns:
            bool: 유효성 여부
        """
        try:
            datetime.strptime(datetime_str, format)
            return True
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def sanitize_sql_input(input_str):
        """
        SQL 인젝션 방지를 위한 입력값 정리
        
        Args:
            input_str (str): 입력 문자열
            
        Returns:
            str: 정리된 문자열
        """
        if not input_str or not isinstance(input_str, str):
            return ""
        
        dangerous_patterns = [
            r"'", r'"', r';', r'--', r'/\*', r'\*/', 
            r'\bUNION\b', r'\bSELECT\b', r'\bINSERT\b', 
            r'\bUPDATE\b', r'\bDELETE\b', r'\bDROP\b'
        ]
        
        sanitized = input_str.strip()
        
        for pattern in dangerous_patterns:
            sanitized = re.sub(pattern, '', sanitized, flags=re.IGNORECASE)
        
        return sanitized
    
    @staticmethod
    def validate_input_length(input_str, min_length=0, max_length=255):
        """
        입력값 길이 검증
        
        Args:
            input_str (str): 입력 문자열
            min_length (int): 최소 길이
            max_length (int): 최대 길이
            
        Returns:
            bool: 유효성 여부
        """
        if not isinstance(input_str, str):
            return False
        
        length = len(input_str.strip())
        return min_length <= length <= max_length
    
    @staticmethod
    def is_numeric_string(input_str):
        """
        숫자 문자열 여부 확인
        
        Args:
            input_str (str): 입력 문자열
            
        Returns:
            bool: 숫자 문자열 여부
        """
        try:
            float(input_str)
            return True
        except (ValueError, TypeError):
            return False
    
    @staticmethod
    def validate_equipment_status(status):
        """
        장비 상태값 유효성 검증
        
        Args:
            status (str): 장비 상태
            
        Returns:
            bool: 유효성 여부
        """
        valid_statuses = ['RUN', 'IDLE', 'DOWN', 'MAINT', 'SETUP', 'STOP']
        return status and status.upper() in valid_statuses