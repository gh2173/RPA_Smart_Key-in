"""
데이터베이스 연결 설정 모듈
"""

class DatabaseConfig:
    """데이터베이스 연결 정보를 관리하는 클래스"""
    
    MES_CONFIG = {
        'host': 'mes.nepes.co.kr',
        'port': '1521',
        'service_name': 'CCUBE',
        'username': 'mighty',
        'password': 'mighty',
        'dsn': 'mes.nepes.co.kr:1521/CCUBE'
    }
    
    NMES_CONFIG = {
        'host': '192.168.222.113',
        'port': '1522', 
        'service_name': 'MOSDB',
        'username': 'nMES',
        'password': 'nMES',
        'dsn': '192.168.222.113:1522/MOSDB'
    }
    
    ERP_CONFIG = {
        'host': '192.168.223.13',
        'port': '1521',
        'service_name': 'ERPSIMAX',
        'username': 'RPA',
        'password': 'RPA',
        'dsn': '192.168.223.13:1521/ERPSIMAX'
    }
    
    @classmethod
    def get_connection_string(cls, db_type='MES'):
        """
        데이터베이스 타입에 따른 연결 문자열 반환
        
        Args:
            db_type (str): 'MES', 'NMES', 'ERP' 중 하나
            
        Returns:
            str: 데이터베이스 연결 문자열
        """
        config_map = {
            'MES': cls.MES_CONFIG,
            'NMES': cls.NMES_CONFIG,
            'ERP': cls.ERP_CONFIG
        }
        
        if db_type not in config_map:
            raise ValueError(f"지원하지 않는 데이터베이스 타입: {db_type}")
            
        config = config_map[db_type]
        return f"{config['username']}/{config['password']}@{config['dsn']}"
    
    @classmethod
    def get_config(cls, db_type='MES'):
        """
        데이터베이스 설정 딕셔너리 반환
        
        Args:
            db_type (str): 'MES', 'NMES', 'ERP' 중 하나
            
        Returns:
            dict: 데이터베이스 설정 정보
        """
        config_map = {
            'MES': cls.MES_CONFIG,
            'NMES': cls.NMES_CONFIG,
            'ERP': cls.ERP_CONFIG
        }
        
        if db_type not in config_map:
            raise ValueError(f"지원하지 않는 데이터베이스 타입: {db_type}")
            
        return config_map[db_type].copy()