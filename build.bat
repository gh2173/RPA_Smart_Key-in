@echo off
REM RPA Smart Key-in Manager 빌드 스크립트 (Windows)

echo ================================================
echo    RPA Smart Key-in Manager 빌드 시작
echo ================================================

REM 현재 디렉토리 확인
echo 📁 작업 디렉토리: %CD%

REM Python 설치 확인
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo ❌ Python이 설치되어 있지 않습니다!
    echo https://www.python.org/downloads/ 에서 Python을 설치하세요.
    pause
    exit /b 1
)

REM PyInstaller 설치 확인
pip show pyinstaller >nul 2>&1
if %errorlevel% neq 0 (
    echo 📦 PyInstaller를 설치합니다...
    pip install pyinstaller
    if %errorlevel% neq 0 (
        echo ❌ PyInstaller 설치 실패!
        pause
        exit /b 1
    )
)

REM 빌드 실행
echo 🚀 빌드를 시작합니다...
pyinstaller --onefile --windowed --name="RPA_Smart_Key-in_Manager" RPA_Smart_Key_in_Manager_250801_4.py

if %errorlevel% eq 0 (
    echo.
    echo ✅ 빌드 성공!
    echo 📁 출력 파일: dist\RPA_Smart_Key-in_Manager.exe
    
    REM 파일 크기 표시
    if exist "dist\RPA_Smart_Key-in_Manager.exe" (
        for %%I in ("dist\RPA_Smart_Key-in_Manager.exe") do (
            set /a size_mb=%%~zI/1048576
            echo 📊 파일 크기: !size_mb! MB
        )
    )
    
    echo.
    echo 🎉 빌드 완료!
    echo dist 폴더의 .exe 파일을 실행하세요.
    
) else (
    echo ❌ 빌드 실패!
    echo 오류를 확인하고 다시 시도하세요.
)

echo.
echo 임시 파일 정리를 원하면 'clean.bat'을 실행하세요.
pause