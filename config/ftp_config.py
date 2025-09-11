"""
FTP 서버 연결 설정 모듈
"""

class FTPConfig:
    """FTP 서버 연결 정보를 관리하는 클래스"""
    
    SERVER_CONFIG = {
        'host': '192.168.223.225',
        'username': 'vega',
        'password': 'vegagcc',
        'port': 21,
        'timeout': 30
    }
    
    UPDATE_PATHS = {
        'remote_directory': '/',
        'version_file': 'version.txt',
        'changelog_file': 'changelog.txt'
    }
    
    @classmethod
    def get_server_config(cls):
        """
        FTP 서버 설정 정보 반환
        
        Returns:
            dict: FTP 서버 연결 설정
        """
        return cls.SERVER_CONFIG.copy()
    
    @classmethod
    def get_connection_info(cls):
        """
        FTP 연결에 필요한 기본 정보 반환
        
        Returns:
            tuple: (host, username, password)
        """
        config = cls.SERVER_CONFIG
        return config['host'], config['username'], config['password']
    
    @classmethod
    def get_update_paths(cls):
        """
        업데이트 관련 파일 경로 정보 반환
        
        Returns:
            dict: 업데이트 파일 경로 정보
        """
        return cls.UPDATE_PATHS.copy()
    
    @classmethod
    def get_version_file_path(cls):
        """
        버전 파일 경로 반환
        
        Returns:
            str: 버전 파일 경로
        """
        return cls.UPDATE_PATHS['version_file']
    
    @classmethod
    def get_changelog_file_path(cls):
        """
        변경로그 파일 경로 반환
        
        Returns:
            str: 변경로그 파일 경로
        """
        return cls.UPDATE_PATHS['changelog_file']