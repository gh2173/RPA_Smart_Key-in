"""
RPA Smart Key-in Manager 메인 애플리케이션
"""

import sys
import os
from PyQt5 import QtWidgets

def setup_environment():
    """환경 설정"""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    sys.path.insert(0, current_dir)

def main():
    """메인 함수"""
    setup_environment()
    
    try:
        from RPA_Smart_Key_in_Manager_250801_4 import MyWindow
        
        app = QtWidgets.QApplication(sys.argv)
        app.setApplicationName("RPA Smart Key-in Manager")
        app.setApplicationVersion("1.0.0")
        
        window = MyWindow()
        window.show()
        
        sys.exit(app.exec_())
        
    except Exception as e:
        print(f"애플리케이션 시작 중 오류 발생: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()