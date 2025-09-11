@echo off
REM 빌드 임시 파일 정리 스크립트

echo 🧹 빌드 임시 파일을 정리합니다...

REM build 폴더 삭제
if exist "build" (
    rmdir /s /q "build"
    echo ✅ 삭제: build\
)

REM __pycache__ 폴더 삭제
if exist "__pycache__" (
    rmdir /s /q "__pycache__"
    echo ✅ 삭제: __pycache__\
)

REM .spec 파일 삭제
for %%f in (*.spec) do (
    del "%%f"
    echo ✅ 삭제: %%f
)

echo.
echo ✅ 정리 완료!
pause