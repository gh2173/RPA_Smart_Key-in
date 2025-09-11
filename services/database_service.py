"""
데이터베이스 서비스 모듈 - 데이터베이스 연결 및 쿼리 관련 기능
"""

import cx_Oracle
import pyodbc
from config.database_config import DatabaseConfig


class DatabaseService:
    """데이터베이스 연결 및 쿼리 처리 서비스"""
    
    def __init__(self):
        """DatabaseService 초기화"""
        self.connection = None
        self.cursor = None
        
    def connect_to_oracle(self, db_type='MES'):
        """
        Oracle 데이터베이스 연결
        
        Args:
            db_type (str): 연결할 데이터베이스 타입 ('MES', 'NMES', 'ERP')
            
        Returns:
            bool: 연결 성공 여부
        """
        try:
            connection_string = DatabaseConfig.get_connection_string(db_type)
            self.connection = cx_Oracle.connect(connection_string)
            self.cursor = self.connection.cursor()
            print(f"{db_type} 데이터베이스 연결 성공")
            return True
        except Exception as e:
            print(f"{db_type} 데이터베이스 연결 실패: {e}")
            return False
    
    def connect_to_odbc(self, connection_string):
        """
        ODBC 데이터베이스 연결
        
        Args:
            connection_string (str): ODBC 연결 문자열
            
        Returns:
            bool: 연결 성공 여부
        """
        try:
            self.connection = pyodbc.connect(connection_string)
            self.cursor = self.connection.cursor()
            print("ODBC 데이터베이스 연결 성공")
            return True
        except Exception as e:
            print(f"ODBC 데이터베이스 연결 실패: {e}")
            return False
    
    def execute_query(self, query, params=None):
        """
        쿼리 실행
        
        Args:
            query (str): 실행할 SQL 쿼리
            params (tuple, optional): 쿼리 매개변수
            
        Returns:
            list: 쿼리 결과 (SELECT) 또는 None (INSERT/UPDATE/DELETE)
        """
        if not self.cursor:
            print("데이터베이스 연결이 없습니다.")
            return None
            
        try:
            if params:
                self.cursor.execute(query, params)
            else:
                self.cursor.execute(query)
            
            if query.strip().upper().startswith('SELECT'):
                return self.cursor.fetchall()
            else:
                self.connection.commit()
                return None
                
        except Exception as e:
            print(f"쿼리 실행 오류: {e}")
            self.connection.rollback()
            return None
    
    def execute_many(self, query, param_list):
        """
        대량 쿼리 실행
        
        Args:
            query (str): 실행할 SQL 쿼리
            param_list (list): 매개변수 리스트
            
        Returns:
            bool: 실행 성공 여부
        """
        if not self.cursor:
            print("데이터베이스 연결이 없습니다.")
            return False
            
        try:
            self.cursor.executemany(query, param_list)
            self.connection.commit()
            return True
        except Exception as e:
            print(f"대량 쿼리 실행 오류: {e}")
            self.connection.rollback()
            return False
    
    def get_columns(self):
        """
        마지막 쿼리의 컬럼 정보 반환
        
        Returns:
            list: 컬럼 이름 리스트
        """
        if not self.cursor:
            return []
        
        try:
            return [desc[0] for desc in self.cursor.description]
        except:
            return []
    
    def close(self):
        """데이터베이스 연결 종료"""
        try:
            if self.cursor:
                self.cursor.close()
            if self.connection:
                self.connection.close()
            print("데이터베이스 연결이 종료되었습니다.")
        except Exception as e:
            print(f"연결 종료 중 오류: {e}")
    
    def __enter__(self):
        """컨텍스트 매니저 진입"""
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """컨텍스트 매니저 종료"""
        self.close()


class QueryBuilder:
    """SQL 쿼리 빌더 유틸리티"""
    
    @staticmethod
    def build_select(table, columns='*', where_clause=None, order_by=None, limit=None):
        """
        SELECT 쿼리 빌드
        
        Args:
            table (str): 테이블명
            columns (str|list): 컬럼명
            where_clause (str): WHERE 조건
            order_by (str): 정렬 조건
            limit (int): 제한 개수
            
        Returns:
            str: 생성된 SQL 쿼리
        """
        if isinstance(columns, list):
            columns = ', '.join(columns)
        
        query = f"SELECT {columns} FROM {table}"
        
        if where_clause:
            query += f" WHERE {where_clause}"
        
        if order_by:
            query += f" ORDER BY {order_by}"
        
        if limit:
            query += f" ROWNUM <= {limit}"
        
        return query
    
    @staticmethod
    def build_insert(table, columns, placeholders=None):
        """
        INSERT 쿼리 빌드
        
        Args:
            table (str): 테이블명
            columns (list): 컬럼명 리스트
            placeholders (str): placeholder 문자열
            
        Returns:
            str: 생성된 SQL 쿼리
        """
        if not placeholders:
            placeholders = ', '.join(['?' for _ in columns])
        
        columns_str = ', '.join(columns)
        query = f"INSERT INTO {table} ({columns_str}) VALUES ({placeholders})"
        
        return query
    
    @staticmethod
    def build_update(table, set_clause, where_clause):
        """
        UPDATE 쿼리 빌드
        
        Args:
            table (str): 테이블명
            set_clause (str): SET 절
            where_clause (str): WHERE 절
            
        Returns:
            str: 생성된 SQL 쿼리
        """
        return f"UPDATE {table} SET {set_clause} WHERE {where_clause}"
    
    @staticmethod
    def build_delete(table, where_clause):
        """
        DELETE 쿼리 빌드
        
        Args:
            table (str): 테이블명
            where_clause (str): WHERE 절
            
        Returns:
            str: 생성된 SQL 쿼리
        """
        return f"DELETE FROM {table} WHERE {where_clause}"