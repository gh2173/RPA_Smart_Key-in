#!/usr/bin/env python3
"""
RPA Smart Key-in Manager 빌드 스크립트
"""

import subprocess
import sys
import os
import shutil
from datetime import datetime

def main():
    """메인 빌드 함수"""
    print("🚀 RPA Smart Key-in Manager 빌드를 시작합니다...")
    
    # 빌드 설정
    script_name = "RPA_Smart_Key_in_Manager_250801_4.py"
    output_name = "RPA_Smart_Key-in_Manager"
    
    # 빌드 명령어 구성
    cmd = [
        "pyinstaller",
        "--onefile",           # 단일 파일로 빌드
        "--windowed",          # 콘솔창 숨기기
        f"--name={output_name}",  # 출력 파일명 지정
        script_name
    ]
    
    # UI 파일이 있다면 포함
    if os.path.exists("RPA_UI.ui"):
        cmd.extend(["--add-data", "RPA_UI.ui;."])
        print("✅ UI 파일 포함: RPA_UI.ui")
    
    print(f"📝 빌드 명령어: {' '.join(cmd)}")
    print("-" * 50)
    
    try:
        # PyInstaller 실행
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)
        
        print("✅ 빌드 성공!")
        print(f"📁 출력 위치: dist/{output_name}.exe")
        
        # 파일 크기 확인
        exe_path = f"dist/{output_name}.exe"
        if os.path.exists(exe_path):
            size_mb = os.path.getsize(exe_path) / (1024 * 1024)
            print(f"📊 파일 크기: {size_mb:.1f} MB")
        
        print("\n🎉 빌드 완료!")
        print(f"실행 파일: {exe_path}")
        
    except subprocess.CalledProcessError as e:
        print("❌ 빌드 실패!")
        print(f"오류: {e}")
        if e.stdout:
            print(f"출력: {e.stdout}")
        if e.stderr:
            print(f"에러: {e.stderr}")
        sys.exit(1)
    
    except FileNotFoundError:
        print("❌ PyInstaller를 찾을 수 없습니다!")
        print("다음 명령어로 설치하세요:")
        print("pip install pyinstaller")
        sys.exit(1)

def clean_build():
    """빌드 임시 파일 정리"""
    print("🧹 빌드 임시 파일을 정리합니다...")
    
    dirs_to_clean = ["build", "__pycache__"]
    files_to_clean = ["*.spec"]
    
    for dir_name in dirs_to_clean:
        if os.path.exists(dir_name):
            shutil.rmtree(dir_name)
            print(f"✅ 삭제: {dir_name}/")
    
    import glob
    for pattern in files_to_clean:
        for file_path in glob.glob(pattern):
            os.remove(file_path)
            print(f"✅ 삭제: {file_path}")

if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "clean":
        clean_build()
    else:
        main()
        print("\n💡 임시 파일을 정리하려면 'python build.py clean'을 실행하세요.")