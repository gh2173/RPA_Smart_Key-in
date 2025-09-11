# RPA Smart Key-in Manager - 모듈화 구조

## 개요
기존의 단일 Jupyter 노트북 파일을 여러 개의 모듈로 분리하여 유지보수성과 확장성을 향상시킨 프로젝트입니다.

## 프로젝트 구조

```
RPA_Smart_Key-in/
├── main.py                                    # 애플리케이션 진입점
├── RPA_Smart_Key_in_Manager_250801_4.py      # 변환된 메인 로직 (기존 .ipynb)
├── RPA_UI.py                                  # UI 정의 파일
├── config/                                    # 설정 관리
│   ├── __init__.py
│   ├── database_config.py                     # 데이터베이스 연결 설정
│   └── ftp_config.py                         # FTP 서버 설정
├── services/                                  # 비즈니스 로직 서비스
│   ├── __init__.py
│   ├── database_service.py                   # 데이터베이스 연결 및 쿼리
│   ├── ftp_service.py                        # FTP 업데이트 기능
│   └── update_service.py                     # 애플리케이션 업데이트
├── ui/                                        # UI 컴포넌트
│   ├── __init__.py
│   └── widgets/
│       ├── __init__.py
│       └── loading_overlay.py                # 로딩 오버레이 위젯
└── utils/                                     # 유틸리티 함수
    ├── __init__.py
    ├── file_utils.py                         # 파일 처리 유틸리티
    └── validation_utils.py                   # 데이터 검증 유틸리티
```

## 모듈별 설명

### 1. config/ - 설정 관리
- **database_config.py**: 데이터베이스 연결 정보 (MES, NMES, ERP)
- **ftp_config.py**: FTP 서버 연결 정보 및 업데이트 경로

### 2. services/ - 비즈니스 로직
- **database_service.py**: 데이터베이스 연결, 쿼리 실행, 트랜잭션 관리
- **ftp_service.py**: FTP 업데이트 확인 및 파일 다운로드
- **update_service.py**: 애플리케이션 업데이트 설치 및 관리

### 3. ui/ - 사용자 인터페이스
- **widgets/loading_overlay.py**: 로딩 화면 오버레이 위젯

### 4. utils/ - 유틸리티
- **file_utils.py**: 파일 복사, 백업, 해시 계산, 임시 파일 정리
- **validation_utils.py**: 사용자 입력, 장비 ID, IP 주소 등 검증

## 실행 방법

### 기본 실행
```bash
python main.py
```

### 모듈별 테스트
```bash
# Config 모듈 테스트
python -c "from config import DatabaseConfig, FTPConfig; print('Config 모듈 작동 확인')"

# Utils 모듈 테스트  
python -c "from utils import FileUtils, ValidationUtils; print('Utils 모듈 작동 확인')"

# 데이터베이스 설정 확인
python -c "from config import DatabaseConfig; print(DatabaseConfig.get_connection_string('MES'))"
```

## 주요 기능

### 데이터베이스 연결
```python
from services.database_service import DatabaseService
from config import DatabaseConfig

# MES 데이터베이스 연결
with DatabaseService() as db:
    db.connect_to_oracle('MES')
    results = db.execute_query("SELECT * FROM some_table")
```

### FTP 업데이트
```python
from services.ftp_service import FTPUpdateChecker
from config import FTPConfig

# 업데이트 확인
checker = FTPUpdateChecker()
checker.update_available.connect(lambda v, f, c: print(f"업데이트 가능: {v}"))
checker.start()
```

### 파일 유틸리티
```python
from utils import FileUtils

# 파일 백업과 함께 복사
FileUtils.copy_file_with_backup("source.txt", "destination.txt")

# 파일 해시 계산
hash_value = FileUtils.get_file_hash("myfile.txt", "md5")
```

### 데이터 검증
```python
from utils import ValidationUtils

# 장비 ID 검증
is_valid = ValidationUtils.is_valid_equipment_id("EQP001")

# IP 주소 검증
is_valid_ip = ValidationUtils.is_valid_ip_address("192.168.1.1")
```

## 모듈화 이점

### 1. **유지보수성 향상**
- 기능별로 코드가 분리되어 수정이 용이
- 특정 기능 오류 시 해당 모듈만 수정

### 2. **재사용성**
- 각 모듈을 다른 프로젝트에서도 활용 가능
- 독립적인 테스트 가능

### 3. **확장성**
- 새로운 기능 추가 시 적절한 모듈에 배치
- 기존 코드에 영향 없이 확장

### 4. **코드 가독성**
- 역할별로 분리된 명확한 구조
- import 문으로 의존성 파악 용이

## 향후 계획

### 1. 점진적 모듈화
```python
# 기존 코드에서 점진적으로 모듈 사용
# 예: FTP 기능을 새 모듈로 교체
from services.ftp_service import FTPUpdateChecker  # 새 모듈 사용
# class FTPUpdateChecker: ... (기존 코드 제거)
```

### 2. 설정 외부화
- 하드코딩된 설정값들을 config 파일로 이동
- 환경별 설정 파일 지원 (개발/운영)

### 3. 테스트 코드 추가
- 각 모듈별 단위 테스트
- 통합 테스트 시나리오

### 4. 로깅 시스템
- 표준화된 로깅 모듈 추가
- 로그 레벨 및 출력 형식 관리

## 주의사항

1. **기존 코드 호환성**: 현재 기존 .ipynb의 모든 기능이 그대로 동작합니다.
2. **의존성**: PyQt5, cx_Oracle 등 기존 의존성은 그대로 유지됩니다.
3. **점진적 적용**: 새 모듈들은 준비되어 있으며, 필요에 따라 점진적으로 적용 가능합니다.

## 문제 해결

### Import 오류 시
```bash
# Python 경로 확인
python -c "import sys; print(sys.path)"

# 현재 디렉토리를 Python 경로에 추가
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

### 모듈 의존성 확인
```bash
# 모듈별 import 테스트
python -c "from config import *"
python -c "from services import *"  
python -c "from utils import *"
```