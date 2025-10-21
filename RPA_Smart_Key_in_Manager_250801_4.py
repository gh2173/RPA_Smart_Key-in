import sys
from PyQt5 import QtWidgets, uic, QtGui, QtCore
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem, QHeaderView, QLabel, QMessageBox, QDialog, QVBoxLayout, QLineEdit, QTextEdit, QDialogButtonBox
from PyQt5.QtWidgets import QPushButton, QGraphicsDropShadowEffect, QProgressDialog, QComboBox, QHBoxLayout, QWidget
from PyQt5.QtGui import QColor, QBrush, QPainter, QPixmap
from PyQt5.QtCore import Qt, QTimer, QRect
import cx_Oracle
from datetime import datetime
import socket
import math
import tempfile
import subprocess
## vega 접속
import pyodbc
import os
from RPA_UI import Ui_TOTAL

# 모듈화된 컴포넌트 import
from ui.widgets.loading_overlay import LoadingOverlay
# from services.database_service import DatabaseService
# from config import DatabaseConfig, FTPConfig
# from utils import validation_utils, file_utils





class MyWindow(QtWidgets.QMainWindow,Ui_TOTAL):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
       
        
        self.setWindowTitle("RPA Smart Key-in Manager v4.1.0 | Developed by HyperAutomation Team  ")
        self.setFixedSize(1400, 900) 
        
        self.tableWidget = QTableWidget(self)
        self.tableWidget.setGeometry(50, 90, 800, 560)  # 필터와 바로 연결되도록 Y좌표 조정
        self.tableWidget.setColumnCount(5)
        self.tableWidget.setHorizontalHeaderLabels(["EQP_MODEL", "EQP_ID", "EQP_STATUS", "COMMENT", "LOCATION"])
        self.tableWidget.hide()
        
        # NS2/NS3 필터 드롭다운 생성
        self.createCampusFilter()
        
        self.loading_overlay = LoadingOverlay(self)
        self.loading_overlay.hide()
        
        self.grid_layout_2 = self.findChild(QtWidgets.QGridLayout, "gridLayout_2")
        self.grid_layout_2_widget = self.grid_layout_2.parentWidget()
        self.PC_TABLE = self.findChild(QtWidgets.QTableView, "PC_TABLE")
        self.PIB_TABLE = self.findChild(QtWidgets.QTableView, "PIB_TABLE")
        
        # label_5 찾기 추가
        self.label_5 = self.findChild(QtWidgets.QLabel, "label_5")
        
        # PIB_TABLE과 label_5 초기 상태는 표시됨 (일반 장비용)
        if self.PIB_TABLE:
            self.PIB_TABLE.show()
        if self.label_5:
            self.label_5.show()
        
        self.CLOSE_BUTTON_1 = self.findChild(QtWidgets.QPushButton, "CLOSE_BUTTON_1")
        self.CLOSE_BUTTON_1.clicked.connect(self.onCloseButtonClicked)
        
        self.CLOSE_BUTTON_1 = self.findChild(QtWidgets.QPushButton, "CLOSE_BUTTON_1")
        self.CLOSE_BUTTON_1.clicked.connect(self.onCloseButton1Clicked)
         
        self.textBrowser = self.findChild(QtWidgets.QTextBrowser, "textBrowser")
        self.textBrowser_2 = self.findChild(QtWidgets.QTextBrowser, "textBrowser_2")
        self.textBrowser_3 = self.findChild(QtWidgets.QTextBrowser, "textBrowser_3")
        self.textBrowser_4 = self.findChild(QtWidgets.QTextBrowser, "textBrowser_4")
        self.textBrowser_5 = self.findChild(QtWidgets.QTextBrowser, "textBrowser_5")
        self.textBrowser_6 = self.findChild(QtWidgets.QTextBrowser, "textBrowser_6")
        self.textBrowser_7 = self.findChild(QtWidgets.QTextBrowser, "textBrowser_7")
        
        self.closeTableButton = QtWidgets.QPushButton("Close Table", self)
        self.closeTableButton.clicked.connect(self.closeTable)
        self.closeTableButton.hide()  # 초기에는 숨겨둡니다
        
        self.pushButton_2.clicked.connect(self.closeMainWindow)
        
        self.PUSH_CLEAR = self.findChild(QtWidgets.QPushButton, "PUSH_CLEAR")
        self.PUSH_CLEAR.clicked.connect(self.clearMonitorData)
        
        ### PUSH_MONITORING 추가
        self.PUSH_MONITORING = self.findChild(QtWidgets.QPushButton, "PUSH_MONITORING")
        self.PUSH_MONITORING.clicked.connect(self.switchToMonitorTab)

        self.tabWidget = self.findChild(QtWidgets.QTabWidget, "tabWidget") 
        
        
        ### PUSH_HOME 추가    
        self.PUSH_HOME = self.findChild(QtWidgets.QPushButton, "PUSH_HOME")
        self.PUSH_HOME.clicked.connect(self.switchToMainTab)

        self.tabWidget = self.findChild(QtWidgets.QTabWidget, "tabWidget") 
        
        
        self.PUSH_LOT_CHANGE = self.findChild(QtWidgets.QPushButton, "PUSH_LOT_CHANGE")
        self.PUSH_LOT_CHANGE.clicked.connect(lambda: self.showTable("LOT_CHANGE"))
        
        self.PUSH_CONVERSION = self.findChild(QtWidgets.QPushButton, "PUSH_CONVERSION")
        self.PUSH_CONVERSION.clicked.connect(lambda: self.showTable("CONVERSION"))      
        
        self.PUSH_LAST_DIE = self.findChild(QtWidgets.QPushButton, "PUSH_LAST_DIE")
        self.PUSH_LAST_DIE.clicked.connect(lambda: self.showTable("LAST_DIE"))
        
        self.PUSH_RETEST = self.findChild(QtWidgets.QPushButton, "PUSH_RETEST")
        self.PUSH_RETEST.clicked.connect(lambda: self.showTable("RETEST"))
        
        self.RPA_START_3 = self.findChild(QtWidgets.QPushButton, "RPA_START_3")
        self.RPA_START_3.clicked.connect(self.insert_data)  
        
        self.PUSH_MONITORING_DATA = self.findChild(QtWidgets.QPushButton, "PUSH_MONITORING_DATA") 
        self.PUSH_MONITORING_DATA.clicked.connect(lambda: self.showTable("MONITORING"))
        
        self.PUSH_USER_INFO = self.findChild(QtWidgets.QPushButton, "PUSH_USER_INFO")
        self.PUSH_USER_INFO.clicked.connect(self.showUserAndKeyDialog)
        
        
        # 현재 필터 상태 저장 변수
        self.current_campus_filter = "전체"
        
        if self.grid_layout_2_widget:
            self.grid_layout_2_widget.hide()
        
        self.tableWidget.setStyleSheet("""
            QTableWidget {
                background-color: #ffffff;
                alternate-background-color: #f8f8f8;
                selection-background-color: #0078d4;
                selection-color: white;
                gridline-color: #d0d0d0;
                border: 1px solid #a0a0a0;
                border-top: none;
                border-bottom-left-radius: 5px;
                border-bottom-right-radius: 5px;
                border-top-left-radius: 0px;
                border-top-right-radius: 0px;
            }
            QHeaderView::section {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f8f8, stop:0.1 #f0f0f0, 
                    stop:0.9 #e8e8e8, stop:1.0 #e0e0e0);
                padding: 6px;
                border: 1px solid #c0c0c0;
                border-top: none;
                font-weight: bold;
                color: #333333;
            }
            QHeaderView::section:first {
                border-left: none;
            }
            QHeaderView::section:last {
                border-right: none;
            }
        """)
        self.tableWidget.setAlternatingRowColors(True)
        
        self.tableWidget.itemDoubleClicked.connect(self.onItemDoubleClicked)
        
        self.EQP_ID = self.findChild(QtWidgets.QLineEdit, "EQP_ID")
        self.LOT_TABLE = self.findChild(QtWidgets.QTableView, "LOT_TABLE")
        self.STEP_TABLE = self.findChild(QtWidgets.QTableView, "STEP_TABLE")
        
        self.INSERT_BUTTON_1 = self.findChild(QtWidgets.QPushButton, "INSERT_BUTTON_1")
        self.INSERT_BUTTON_1.clicked.connect(self.onInsertButtonClicked)

        self.selected_product = None
        self.selected_lot = None
        self.selected_pc = None
        self.selected_pib = None
        self.skip_pib = False  # PIB 건너뛰기 플래그 추가

        # LOT_TABLE, PC_TABLE, PIB_TABLE의 선택 모드를 행 단위로 설정
        self.LOT_TABLE.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.PC_TABLE.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.PIB_TABLE.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

        self.LOT_TABLE.clicked.connect(self.onLotTableClicked)
        self.PC_TABLE.clicked.connect(self.onPCTableClicked)
        self.PIB_TABLE.clicked.connect(self.onPIBTableClicked)
        
        
        self.ftp_host = '192.168.223.225'
        self.ftp_username = 'vega'
        self.ftp_password = 'vegagcc'
        
        self.STATUS_ID = self.findChild(QtWidgets.QLineEdit, "STATUS_ID")
        
        # EQP_ID와 STATUS_ID 폰트 스타일을 11px로 고정 설정
        if self.EQP_ID and self.STATUS_ID:
            font_11px = QtGui.QFont()
            font_11px.setPointSize(11)
            self.EQP_ID.setFont(font_11px)
            self.STATUS_ID.setFont(font_11px)
        
    
    def createCampusFilter(self):
        """NS2/NS3 필터 드롭다운을 생성합니다"""
        # 필터 위젯 컨테이너 생성
        self.filter_widget = QWidget(self)
        self.filter_widget.setGeometry(50, 50, 800, 40)  # 테이블 위쪽에 배치
        self.filter_widget.hide()
        
        # Windows 헤더 스타일 배경 적용 (테이블과 일체형)
        self.filter_widget.setStyleSheet("""
            QWidget {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f0f0f0, stop:0.1 #e8e8e8, 
                    stop:0.9 #d0d0d0, stop:1.0 #c8c8c8);
                border: 1px solid #a0a0a0;
                border-bottom: none;
                border-top-left-radius: 5px;
                border-top-right-radius: 5px;
                border-bottom-left-radius: 0px;
                border-bottom-right-radius: 0px;
            }
        """)
        
        # 수평 레이아웃 생성
        filter_layout = QHBoxLayout(self.filter_widget)
        filter_layout.setContentsMargins(10, 8, 10, 8)  # 여백 추가
        
        # 라벨 생성
        filter_label = QLabel("📍 Campus Filter:")
        filter_label.setStyleSheet("""
            QLabel {
                font-size: 14px;
                font-weight: bold;
                color: #333333;
                background: transparent;
                border: none;
                padding: 2px 8px;
            }
        """)
        
        # 드롭다운 콤보박스 생성
        self.campus_filter = QComboBox()
        self.campus_filter.addItems(["전체", "NS2", "NS3"])
        self.campus_filter.setCurrentText("전체")
        
        # Windows 스타일 콤보박스 적용
        self.campus_filter.setStyleSheet("""
            QComboBox {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ffffff, stop:0.1 #f8f8f8, 
                    stop:0.9 #e0e0e0, stop:1.0 #d8d8d8);
                color: #333333;
                font-size: 13px;
                font-weight: bold;
                padding: 6px 12px;
                border: 1px solid #999999;
                border-radius: 3px;
                min-width: 100px;
            }
            QComboBox:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f0f8ff, stop:0.1 #e8f4ff, 
                    stop:0.9 #d0e8ff, stop:1.0 #c8e0ff);
                border: 1px solid #0078d4;
            }
            QComboBox:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #e0e8f0, stop:1.0 #c0d0e0);
            }
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid #999999;
                background: transparent;
            }
            QComboBox::down-arrow {
                image: none;
                border: 1px solid #666666;
                width: 0px;
                height: 0px;
                border-top: 5px solid #666666;
                border-left: 3px solid transparent;
                border-right: 3px solid transparent;
                margin: 3px;
            }
            QComboBox QAbstractItemView {
                background-color: white;
                color: #333333;
                selection-background-color: #0078d4;
                selection-color: white;
                border: 1px solid #999999;
                font-size: 13px;
                outline: 0;
            }
        """)
        
        # 필터 변경 시 이벤트 연결
        self.campus_filter.currentTextChanged.connect(self.onCampusFilterChanged)
        
        # 레이아웃에 위젯 추가
        filter_layout.addWidget(filter_label)
        filter_layout.addWidget(self.campus_filter)
        filter_layout.addStretch()  # 나머지 공간 채우기
        
        self.filter_widget.setLayout(filter_layout)
    
    def onCampusFilterChanged(self, filter_value):
        """Campus 필터 변경 시 호출되는 이벤트 핸들러"""
        self.current_campus_filter = filter_value
        print(f"Campus 필터 변경: {filter_value}")
        
        # 현재 표시된 테이블이 있으면 필터 재적용
        if hasattr(self, 'current_action') and self.tableWidget.isVisible():
            # 로딩 표시
            self.loading_overlay.setGeometry(self.rect())
            self.loading_overlay.show()
            # 쿼리 재실행
            QTimer.singleShot(100, self.executeQuery)
        

    def is_utc_equipment(self, eqp_id):
        """UTC59~UTC73 범위의 장비인지 확인"""
        if not eqp_id.startswith('UTC'):
            return False
        
        try:
            # UTC 뒤의 숫자 추출
            number = int(eqp_id[3:])
            return 59 <= number <= 73
        except (ValueError, IndexError):
            return False
        
    def onRPAStartClicked(self):
        # Monitor 탭의 데이터 수집
        monitor_data = {
            "DEVICE": self.textBrowser.toPlainText(),
            "LOT-ID": self.textBrowser_2.toPlainText(),
            "STEP-ID": self.textBrowser_3.toPlainText(),
            "PC-ID": self.textBrowser_4.toPlainText(),
            "PB-ID": self.textBrowser_5.toPlainText(),
            "COMMENT": self.textBrowser_7.toPlainText()  
        }

        # 모든 필드가 채워져 있는지 확인
        if not all(monitor_data.values()):
            QtWidgets.QMessageBox.warning(self, "경고", "Please fill in all the fields.")
            return

        # AUTOBE MAT Plus 실행
        import os
        cmd = r'"C:\Program Files\AUTOBE MAT Plus\AUTOBE MAT Plus.exe" -a "D:\Project\NepesArkDemo\NepesArkDemo.amproj" -s "conversion" -t'
        os.popen(cmd)
        
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("RPA 시작")
        layout = QtWidgets.QVBoxLayout()

        # Monitor 데이터 표시
        for key, value in monitor_data.items():
            label = QtWidgets.QLabel(f"{key}: {value}")
            layout.addWidget(label)

        user_id_label = QtWidgets.QLabel("USER-ID를 입력하세요.")
        user_id_input = QtWidgets.QLineEdit()
        layout.addWidget(user_id_label)
        layout.addWidget(user_id_input)

        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        # 'OK' 버튼 비활성화
        ok_button = button_box.button(QtWidgets.QDialogButtonBox.Ok)
        ok_button.setEnabled(False)

        def validate_user_id(text):
            if text.isdigit() and len(text) == 8:
                ok_button.setEnabled(True)
            else:
                ok_button.setEnabled(False)

        user_id_input.textChanged.connect(validate_user_id)

        dialog.setLayout(layout)

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            user_id = user_id_input.text()
            monitor_data["USER-ID"] = user_id
            self.uploadToAccess(monitor_data)
        else:
            QtWidgets.QMessageBox.warning(self, "취소", "RPA 작업이 취소되었습니다.")


    def switchToMonitorTab(self):
        monitor_tab_index = self.findMonitorTabIndex()
        if monitor_tab_index != -1:
            self.tabWidget.setCurrentIndex(monitor_tab_index)
            #if hasattr(self, 'current_action') and self.STATUS_ is not None:
             #   self.STATUS_.setText(self.current_action)
            #elif self.STATUS_ is None:
            #    print("Warning: STATUS_ widget is None")
        #else:
         #   QtWidgets.QMessageBox.warning(self, "경고", "Monitor 탭을 찾을 수 없습니다.")

    def findMonitorTabIndex(self):
        for i in range(self.tabWidget.count()):
            if self.tabWidget.tabText(i) == "Monitor":
                return i
        return -1
    
    def switchToMainTab(self):
        main_tab_index = self.findMainTabIndex()
        if main_tab_index != -1:
            self.tabWidget.setCurrentIndex(main_tab_index)
        else:
            QtWidgets.QMessageBox.warning(self, "경고", "Main 탭을 찾을 수 없습니다.")

    def findMainTabIndex(self):
        for i in range(self.tabWidget.count()):
            if self.tabWidget.tabText(i) == "Main":
                return i
        return -1
    
    def switchToReferenceTab(self):
        reference_tab_index = self.findReferenceTabIndex()
        if reference_tab_index != -1:
            self.tabWidget.setCurrentIndex(reference_tab_index)
        else:
            QtWidgets.QMessageBox.warning(self, "경고", "Reference 탭을 찾을 수 없습니다.")

    def findReferenceTabIndex(self):
        for i in range(self.tabWidget.count()):
            if self.tabWidget.tabText(i) == "Reference":
                return i
        return -1
            
    def switchToMonitorTab(self):
        monitor_tab_index = self.findMonitorTabIndex()
        if monitor_tab_index != -1:
            self.tabWidget.setCurrentIndex(monitor_tab_index)
        else:
            QtWidgets.QMessageBox.warning(self, "경고", "Monitor 탭을 찾을 수 없습니다.")

    def findMonitorTabIndex(self):
        for i in range(self.tabWidget.count()):
            if self.tabWidget.tabText(i) == "Monitor":
                return i
        return -1
    

    def clearMonitorData(self):
        # 모든 textBrowser 위젯의 내용을 지웁니다
        self.textBrowser.clear()
        self.textBrowser_2.clear()
        self.textBrowser_3.clear()
        self.textBrowser_4.clear()
        self.textBrowser_5.clear()
        self.textBrowser_6.clear()
        self.textBrowser_7.clear()
        self.EQP_ID.clear()
        self.STATUS_ID.clear()

        # PIB 건너뛰기 플래그 초기화 및 PIB_TABLE, label_5 다시 표시
        self.skip_pib = False
        if self.PIB_TABLE:
            self.PIB_TABLE.show()
        if self.label_5:
            self.label_5.show()

        # 데이터가 성공적으로 지워졌다는 메시지를 표시합니다
        QtWidgets.QMessageBox.information(self, "알림", "Data clearing was successful.")
        
    def showTable(self, action_type):
        self.current_action = action_type  # 현재 액션 저장
        self.STATUS_ID.setText(action_type)  # Monitor 탭의 STATUS_ID에 텍스트 설정
        self.loading_overlay.setGeometry(self.rect())
        self.loading_overlay.show()
        
        # 필터 위젯 표시
        self.filter_widget.show()
        
        QTimer.singleShot(100, self.executeQuery)
        self.closeTableButton.show()
    
    def onCloseButtonClicked(self):
        if self.grid_layout_2_widget:
            self.grid_layout_2_widget.hide()
        if self.tableWidget.isVisible():
            self.tableWidget.show()
            self.closeTableButton.show()
        else:
            self.tableWidget.hide()
            self.closeTableButton.hide()
            
    def onCloseButton1Clicked(self):
        main_tab_index = self.findMainTabIndex()
        if main_tab_index != -1:
            self.tabWidget.setCurrentIndex(main_tab_index)
        else:
            QtWidgets.QMessageBox.warning(self, "경고", "Main 탭을 찾을 수 없습니다.")

    def findMainTabIndex(self):
        for i in range(self.tabWidget.count()):
            if self.tabWidget.tabText(i).lower() == "main":
                return i
        return -1

    def createButton(self):
        self.closeTableButton = QPushButton("✕ Close Table", self)
        self.closeTableButton.clicked.connect(self.closeTable)
        
        # 테이블과 일체감 있는 스타일 적용
        self.closeTableButton.setStyleSheet("""
            QPushButton {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #f8f8f8, stop:0.1 #f0f0f0, 
                    stop:0.9 #e8e8e8, stop:1.0 #e0e0e0);
                color: #333333;
                font-size: 12px;
                font-weight: bold;
                padding: 8px 16px;
                border: 1px solid #a0a0a0;
                border-top: none;
                border-bottom-left-radius: 0px;
                border-bottom-right-radius: 5px;
                border-top-left-radius: 0px;
                border-top-right-radius: 0px;
            }
            QPushButton:hover {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #ff6b6b, stop:0.1 #ff5252, 
                    stop:0.9 #e53935, stop:1.0 #d32f2f);
                color: white;
                border: 1px solid #c62828;
            }
            QPushButton:pressed {
                background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                    stop:0 #d32f2f, stop:1.0 #b71c1c);
                color: white;
            }
        """)
        
        
    def executeQuery(self):
        # 데이터베이스 연결 정보 수정
        # dsn_tns = cx_Oracle.makedsn('192.168.223.13', 1521, service_name='ERPSIMAX')
        # connection = cx_Oracle.connect(user='RPA', password='rpa01!', dsn=dsn_tns)
        # cursor = connection.cursor()
        
        dsn = cx_Oracle.makedsn("mes.nepes.co.kr", 1521, "CCUBE")
        connection = cx_Oracle.connect("mighty", "mighty", dsn)
        cursor = connection.cursor()
    
        #  수정가능 -->   RPA_ADMIN.view_eqpsts
        # DB
        query = """
            SELECT *
                FROM(
                    SELECT
                    s.PLANT, s.EQUIPMENT_ID, s.MAIN_STATUS, s.USER_COMMENT, s.TRANS_TIME,
                    CASE
                        /* T2K -NS3 */
                        WHEN s.EQUIPMENT_ID IN (
                            'T2K75','T2K76','T2K85','T2K93','T2K94','T2K95','T2K98','T2K99',
                            'T2K100','T2K101','T2K102','T2K103','T2K104','T2K105','T2K106'
                        ) THEN 'NS3'
                        /* T2K-NS2 */
                        WHEN s.EQUIPMENT_ID LIKE '%T2K%' THEN 'NS2'
                        /* U-FLEX-NS2 */
                        WHEN s.EQUIPMENT_ID IN (
                            'UTS04', 'UTS05', 'UTS06', 'UTS07', 'UTS08', 'UTSP08', 'UTS09', 'UTSP09', 'UTS10') THEN 'NS2'
                        /* U-FLEX-XD */  
                        WHEN s.EQUIPMENT_ID LIKE '%UTS%' THEN 'NS3'
                        /* U-FLEX-PLUS */
                        WHEN s.EQUIPMENT_ID LIKE '%UTC%' THEN 'NS3'
                        /* ETS600 */
                        WHEN s.EQUIPMENT_ID LIKE '%ETS%'
                        AND LENGTH(s.EQUIPMENT_ID) = 5 THEN 'NS2'
                        /*V93K */
                        WHEN s.EQUIPMENT_ID LIKE '%V93K%' THEN 'NS3'
                        /*ND4 */
                        WHEN s.EQUIPMENT_ID LIKE '%ND4%' THEN 'NS3'
                        /*DIAMONDX */
                        WHEN s.EQUIPMENT_ID LIKE '%DMX%' THEN 'NS3'
                        /* ���� �� ��: NULL ���� */
                        ELSE NULL
                    END AS CAMPUS
                FROM (
                    SELECT
                        e.*,
                        ROW_NUMBER() OVER (
                            PARTITION BY e.EQUIPMENT_ID
                            ORDER BY TO_DATE(e.TRANS_TIME, 'YYYYMMDD HH24MISS') DESC
                        ) AS rn
                    FROM EQPSTS e
                ) s
                WHERE s.rn = 1
                ) x

                WHERE x.CAMPUS IS NOT NULL
                AND x.PLANT IN 'CCUBEDIGITAL'
                AND x.MAIN_STATUS NOT IN ('RUN', 'SHUTDOWN')
            """
        
        # Campus 필터 적용
        if hasattr(self, 'current_campus_filter') and self.current_campus_filter != "전체":
            query += f" AND x.CAMPUS = '{self.current_campus_filter}'"
        
        query += " ORDER BY x.EQUIPMENT_ID"
        
    
        cursor.execute(query)
        results = sorted(cursor.fetchall(), key=lambda x: x[2] if x[2] is not None else '')
    
        # self.tableWidget.setRowCount(len(results))
        # for i, row in enumerate(results):
        #     for j, value in enumerate(row):
        #         item = QTableWidgetItem(str(value))
        #         item.setTextAlignment(Qt.AlignCenter)
        #         self.tableWidget.setItem(i, j, item)
        
        self.tableWidget.setRowCount(len(results))

        for i, row in enumerate(results):

            main_status = row[2]  # MAIN_STATUS 컬럼 (인덱스 2)
            
            # MAIN_STATUS에 따른 색상 설정
            main_status_str = str(main_status).upper() if main_status else ''

            # MAIN_STATUS에 따른 색상 설정
            if main_status == 'LOAD DOWN':
                row_color = QColor('#FFA500')  #주황색
            elif main_status == 'IDLE':
                row_color = QColor('#4169E1')  #로열블루
            elif 'CUS' in main_status_str:
                row_color = QColor('#00FFFF') # 하늘색
            elif 'OM' in main_status_str:
                row_color = QColor('#A52A2A')  #자주색?
            elif 'BM' in main_status_str:
                row_color = QColor('#0000CD') # 파란색
            elif 'PM' in main_status_str:
                row_color = QColor('#F08080') # 분홍색
                
            else:
                row_color = QColor('#FF0000') # 빨간색
                
            for j, value in enumerate(row):
                item = QTableWidgetItem(str(value))
                item.setTextAlignment(Qt.AlignCenter)
                item.setBackground(row_color)  # 행 배경색 설정
                self.tableWidget.setItem(i, j, item)
 
    
        self.tableWidget.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.loading_overlay.hide()
        self.tableWidget.show()
        # 필터와 연결되도록 테이블 위치 조정
        self.tableWidget.setGeometry(50, 90, self.width() - 100, self.height() - 190)
        
        # 필터 위젯 크기 조정
        if hasattr(self, 'filter_widget'):
            self.filter_widget.setGeometry(50, 50, self.width() - 100, 40)
    
        # Close 버튼을 테이블 오른쪽 하단에 붙여서 일체감 연출
        table_right = 50 + (self.width() - 100)  # 테이블 오른쪽 끝
        table_bottom = 90 + (self.height() - 190)  # 테이블 아래쪽 끝
        self.closeTableButton.setGeometry(table_right - 120, table_bottom - 1, 120, 30)
        self.closeTableButton.show()
    
        cursor.close()
        connection.close()
            
    def closeTable(self):
        self.tableWidget.hide()
        self.closeTableButton.hide()
        # 필터 위젯도 숨기기
        if hasattr(self, 'filter_widget'):
            self.filter_widget.hide()
    
    def onItemDoubleClicked(self, item):
        row = item.row()
        eqp_id = self.tableWidget.item(row, 1).text()
        main_status = self.tableWidget.item(row, 2).text()  # MAIN_STATUS 값 가져오기
        
        self.EQP_ID.setText(eqp_id)
        self.tableWidget.hide()
        self.closeTableButton.hide()
        
        # MAIN_STATUS가 'OM'을 포함하는 경우 특별한 처리
        if 'OM' in main_status:
            self.showUserInfoPopup(eqp_id, main_status)
            return
        
        # UTC59~UTC73 장비인지 확인
        self.skip_pib = self.is_utc_equipment(eqp_id)
        
        # PIB 테이블과 label_5 초기 표시 상태 설정
        if not self.skip_pib:
            # 일반 장비는 PIB 테이블과 label_5 표시
            if self.PIB_TABLE:
                self.PIB_TABLE.show()
            if self.label_5:
                self.label_5.show()
        
        if self.grid_layout_2_widget:
            self.grid_layout_2_widget.show()
        
            self.processGridLayout2(eqp_id)
            
            # updateLotAndStepTables 메서드가 성공적으로 실행된 경우에만 ReferenceTab으로 이동
            result = self.updateLotAndStepTables(eqp_id)
            if result:
                self.switchToReferenceTab()  # ReferenceTab으로 이동                
        
        if self.current_action == "MONITORING":
            self.showUserInputDialog(eqp_id)
            
    def showUserInfoPopup(self, eqp_id, main_status):
        """MAIN_STATUS가 'OM'을 포함하는 경우 USERINFO 입력 팝업창"""
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("USERINFO 입력")
        dialog.resize(350, 200)
        layout = QtWidgets.QVBoxLayout()

        # 스타일 시트 설정
        dialog.setStyleSheet("""
            QDialog {
                background-color: #f0f0f0;
                border: 1px solid #c0c0c0;
                border-radius: 10px;
            }
            QLabel {
                font-size: 14pt;
                font-weight: bold;
                color: #333333;
            }
            QLineEdit {
                font-size: 12pt;
                padding: 5px;
                border: 1px solid #c0c0c0;
                border-radius: 5px;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                font-size: 12pt;
                margin: 4px 2px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:disabled {
                background-color: gray;
                color: white;
            }
        """)

        # 안내 레이블
        info_label = QtWidgets.QLabel(f"장비 ID: {eqp_id}")
        info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_label)

        # USERINFO 입력 필드
        user_info_label = QtWidgets.QLabel("USERINFO (8자리 숫자):")
        user_info_input = QtWidgets.QLineEdit()
        user_info_input.setMaxLength(8)  # 8자리 제한
        layout.addWidget(user_info_label)
        layout.addWidget(user_info_input)

        # 버튼 박스
        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        # OK 버튼 초기 비활성화
        ok_button = button_box.button(QtWidgets.QDialogButtonBox.Ok)
        ok_button.setEnabled(False)

        # 입력값 유효성 검사
        def validate_user_info(text):
            if text.isdigit() and len(text) == 8:
                ok_button.setEnabled(True)
            else:
                ok_button.setEnabled(False)

        user_info_input.textChanged.connect(validate_user_info)

        dialog.setLayout(layout)

        # 팝업창 실행
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            user_info = user_info_input.text()
            self.insertMonitorData(eqp_id, main_status, user_info)
        else:
            QtWidgets.QMessageBox.information(self, "취소", "USERINFO 입력이 취소되었습니다.")
            
    def insertMonitorData(self, eqp_id, main_status, user_info):
        """Monitor Tab에 데이터 입력 - OM 모드용으로 수정"""
        # EQP_ID 객체에 DB의 EQP_ID 값 입력
        self.EQP_ID.setText(eqp_id)
        
        # STATUS_ID 객체에 'OM' 고정값 입력하고 폰트 크기를 11px로 설정
        self.STATUS_ID.setText('OM')
        
        # STATUS_ID 폰트를 11px로 고정 설정
        font_11px = QtGui.QFont()
        font_11px.setPointSize(11)
        self.STATUS_ID.setFont(font_11px)
        
        # textBrowser_6에 8자리 숫자 입력
        self.textBrowser_6.setText(user_info)
        
        # 나머지 textBrowser 객체들은 모두 공란으로 설정
        self.textBrowser.clear()
        self.textBrowser_2.clear()
        self.textBrowser_3.clear()
        self.textBrowser_4.clear()
        self.textBrowser_5.clear()
        self.textBrowser_7.clear()

        QtWidgets.QMessageBox.information(self, "완료", f"Monitor Tab에 데이터가 입력되었습니다.\n\nEQP_ID: {eqp_id}\nSTATUS: OM\nUSER_ID: {user_info}")
        
        # Monitor Tab으로 이동
        self.switchToMonitorTab()
          
    def processGridLayout2(self, eqp_id):
        if self.grid_layout_2:
            print(f"Processing gridLayout_2 for EQP_ID: {eqp_id}")
            
            for i in range(self.grid_layout_2.rowCount()):
                for j in range(self.grid_layout_2.columnCount()):
                    item = self.grid_layout_2.itemAtPosition(i, j)
                    if item:
                        widget = item.widget()
                        if widget:
                            print(f"Widget at ({i}, {j}): {widget}")
            
    def updateLotAndStepTables(self, eqp_id):
        try:
            dialog = QDialog(self)
            dialog.setWindowTitle(f"LOT_ID 입력 - {eqp_id}")
            dialog.resize(300, 150)  # 팝업 레이아웃 사이즈를 늘립니다
            layout = QVBoxLayout()

            # 스타일 시트 설정
            dialog.setStyleSheet("""
                QDialog {
                    background-color: #f0f0f0;
                    border: 1px solid #c0c0c0;
                    border-radius: 10px;
                }
                QLabel {
                    font-size: 14pt;
                    font-weight: bold;
                    color: #333333;
                }
                QLineEdit {
                    font-size: 12pt;
                    padding: 5px;
                    border: 1px solid #c0c0c0;
                    border-radius: 5px;
                }
                QDialogButtonBox {
                    font-size: 12pt;
                }
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;
                    font-size: 12pt;
                    margin: 4px 2px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QPushButton:pressed {
                    background-color: #3e8e41;
                }
            """)

            lot_id_label = QLabel("LOT_ID:")
            lot_id_input = QLineEdit()
            layout.addWidget(lot_id_label)
            layout.addWidget(lot_id_input)

            button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            button_box.accepted.connect(dialog.accept)
            button_box.rejected.connect(lambda: (dialog.reject(), self.switchToMainTab()))  # Cancel 버튼을 누르면 Main_tab으로 이동
            layout.addWidget(button_box)

            dialog.setLayout(layout)

            if dialog.exec_() == QDialog.Accepted:
                lot_id = lot_id_input.text()
                if not lot_id:
                    QMessageBox.warning(self, "경고", "LOT_ID를 입력해주세요.")
                    return False

                dsn = cx_Oracle.makedsn("192.168.222.113", 1522, service_name="MOSDB")
                connection = cx_Oracle.connect("nMES", "mesn0123!", dsn)
                cursor = connection.cursor()

                # DB 요청해야됨
                query = """
                SELECT PRODUCT, STEP_SEQ, LOT_ID, STATUS, LOT_STATUS_SEG
                FROM (
                    SELECT
                        STEP_SEQ,
                        LOT_ID,
                        STEP_STATUS_SEG AS STATUS,
                        LOT_STATUS_SEG,
                        PROD_ID AS PRODUCT,
                        ROUND((SYSDATE - TO_DATE(REPLACE(LAST_EVENT_DATE, ' ', ' '), 'YYYYMMDDHH24MISS')), 1) AS STEP_정체일,
                        ROW_NUMBER() OVER (PARTITION BY LOT_ID ORDER BY LAST_EVENT_DATE DESC) AS rn
                    FROM SIMAXE.MC_LOT
                    WHERE
                        LOT_ID = :lot_id
                    AND (STEP_SEQ LIKE 'A0%' OR STEP_SEQ LIKE 'Y0%')
                    AND LOT_STATUS_SEG IN ('Active', 'Hold')
                )
                WHERE rn = 1
                ORDER BY STEP_SEQ ASC
                """

                cursor.execute(query, {'lot_id': lot_id})
                results = cursor.fetchall()

                # 'STATUS' 컬럼값에 'RUN'이 포함되어 있을 때 인터락 추가
                if any('RUN' in row[3] for row in results):
                    QMessageBox.warning(self, "경고", "해당 LOT_ID는 현재 'RUN' 상태입니다.")
                    cursor.close()
                    connection.close()
                    self.Main_tab()
                    return False

                # 'STEP_SEQ' 컬럼값이 지정된 조건이 아닐 때 인터락 추가
                valid_steps = ['A02450', 'A02500', 'A02650', 'A02750', 'A02450TR01', 'A02500TR01', 'A02650TR01', 'A02750TR01'
                                , 'Y06000', 'Y06320', 'Y06420', 'Y06475', 'Y06000TR01', 'Y06320TR01', 'Y06420TR01', 'Y06475TR01']            
                if not any(row[1] in valid_steps for row in results):
                    QMessageBox.warning(self, "경고", "해당 LOT_ID가 존재하지 않거나 지정된 STEP에서 찾을 수 없습니다.")
                    cursor.close()
                    connection.close()
                    self.Main_tab()
                    return False
                
                # 'LOT_STATUS_SEG' 컬럼값이 지정된 조건이 아닐 때 인터락 추가
                if any('Hold' in row[4] for row in results):
                    QMessageBox.warning(self, "경고", "해당 LOT_ID는 'Hold' 상태입니다.")
                    cursor.close()
                    connection.close()
                    self.Main_tab()
                    return False

                # LOT_TABLE 업데이트
                lot_model = QtGui.QStandardItemModel()
                lot_model.setHorizontalHeaderLabels(["PRODUCT", "STEP_SEQ", "LOT_ID", "STATUS", "LOT_STATUS_SEG"])
                for row in results:
                    items = [QtGui.QStandardItem(str(value)) for value in row]

                    # LOT_STATUS_SEG에 따라 행 색상 설정
                    if row[4] == 'Hold':
                        for item in items:
                            item.setBackground(QColor('#eb3737'))  # 빨간색
                    elif row[4] == 'Active':
                        for item in items:
                            item.setBackground(QColor('#37eb73'))  # 초록색

                    lot_model.appendRow(items)

                self.LOT_TABLE.setModel(lot_model)
                self.LOT_TABLE.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

                cursor.close()
                connection.close()

                # LOT_TABLE 업데이트 후 PC_TABLE과 PIB_TABLE도 업데이트
                self.selected_lot = 0  # 첫 번째 행을 선택된 행으로 설정
                self.updatePCTable()
                # UTC59~UTC73 장비가 아닌 경우에만 PIB 테이블 업데이트
                if not self.skip_pib:
                    # 일반 장비는 PIB 테이블과 label_5 표시
                    if self.PIB_TABLE:
                        self.PIB_TABLE.show()
                    if self.label_5:
                        self.label_5.show()
                    self.updatePIBTable()
                else:
                    # UTC59~UTC73 장비인 경우 PIB 테이블과 label_5를 완전히 숨김
                    if self.PIB_TABLE:
                        self.PIB_TABLE.hide()
                    if self.label_5:
                        self.label_5.hide()
                    QMessageBox.information(self, "알림", f"선택된 장비 {eqp_id}는 PIB 입력이 생략됩니다.")

                ###############################################################
                if not results:
                    QMessageBox.information(self, "ERROR", "해당 LOT_ID에 대한 정보가 없습니다.")
                    # 빈 모델을 설정하여 테이블을 비웁니다.
                    empty_model = QtGui.QStandardItemModel()
                    empty_model.setHorizontalHeaderLabels(["PRODUCT", "STEP_SEQ", "LOT_ID", "STATUS", "LOT_STATUS_SEG"])
                    self.LOT_TABLE.setModel(empty_model)
                    return False

                return True
            else:
                QMessageBox.warning(self, "경고", "LOT_ID 입력이 취소되었습니다.")
                return False
                ###############################################################
        except Exception as e:
            # 예외가 발생하면 에러 메시지를 표시하고 프로그램이 종료되지 않도록 합니다.
            QMessageBox.critical(self, "에러", f"예외가 발생했습니다: {str(e)}")
            return False
        
    def updatePCTable(self):
        try:
            # Probe Card 입력 팝업창 생성
            dialog = QDialog(self)
            dialog.setWindowTitle("Probe Card 입력")
            dialog.resize(300, 150)
            layout = QVBoxLayout()

            # 스타일 시트 설정
            dialog.setStyleSheet("""
                QDialog {
                    background-color: #f0f0f0;
                    border: 1px solid #c0c0c0;
                    border-radius: 10px;
                }
                QLabel {
                    font-size: 14pt;
                    font-weight: bold;
                    color: #333333;
                }
                QLineEdit {
                    font-size: 12pt;
                    padding: 5px;
                    border: 1px solid #c0c0c0;
                    border-radius: 5px;
                }
                QDialogButtonBox {
                    font-size: 12pt;
                }
                QPushButton {
                    background-color: #4CAF50;
                    color: white;
                    border: none;
                    padding: 10px 20px;
                    text-align: center;
                    text-decoration: none;
                    display: inline-block;
                    font-size: 12pt;
                    margin: 4px 2px;
                    border-radius: 5px;
                }
                QPushButton:hover {
                    background-color: #45a049;
                }
                QPushButton:pressed {
                    background-color: #3e8e41;
                }
            """)

            # 입력 필드와 버튼 추가
            probe_card_label = QLabel("Probe Card ID:")
            probe_card_input = QLineEdit()
            layout.addWidget(probe_card_label)
            layout.addWidget(probe_card_input)

            button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
            button_box.accepted.connect(dialog.accept)
            button_box.rejected.connect(dialog.reject)
            layout.addWidget(button_box)

            dialog.setLayout(layout)

            # 팝업창 실행
            if dialog.exec_() == QDialog.Accepted:
                probe_card_id = probe_card_input.text()
                if not probe_card_id:
                    QMessageBox.warning(self, "경고", "Probe Card ID를 입력해주세요.")
                    return

                # 데이터베이스 쿼리 실행 및 결과 필터링
                lot_model = self.LOT_TABLE.model()
                if lot_model is None or self.selected_lot is None:
                    QtWidgets.QMessageBox.warning(self, "경고", "LOT_TABLE에서 항목을 선택해주세요.")
                    return

                product = lot_model.data(lot_model.index(self.selected_lot, 0))  # PRODUCT 컬럼의 값을 가져옵니다.
                product_prefix = product[:7]  # 앞자리 7자리를 추출합니다.
           
                dsn_tns = cx_Oracle.makedsn('192.168.222.113', 1521, service_name='fdryeds')
                connection = cx_Oracle.connect(user='Ark_select_user', password='ark12$select', dsn=dsn_tns)
                cursor = connection.cursor()
                
                # DB
                query = """
                SELECT DISTINCT
                    A.PC_ID,
                    A.PC_GROUP,
                    A.EQP_GROUP AS 설비,
                    A.KEEPING_ROOM AS 위치,
                    A.TOTAL_AGE_SHOT
                FROM EDS_DB.PMS_MAIN A
                LEFT JOIN EDS_DB.PMS_MAIN_PROD B ON A.PC_ID = B.PC_ID
                WHERE SUBSTR(B.PROD, 1, 7) = :product_prefix
                
                ORDER BY PC_ID ASC
                """

                cursor.execute(query, {'product_prefix': product_prefix})
                results = cursor.fetchall()

                # 입력된 Probe Card ID와 비교하여 필터링
                filtered_results = [row for row in results if row[0] == probe_card_id]

                # PC_TABLE 업데이트
                pc_model = QtGui.QStandardItemModel()
                pc_model.setHorizontalHeaderLabels(["PC_ID", "PC_GROUP", "설비", "위치", "TOTAL_SHOT"])
                for row in filtered_results:
                    items = [QtGui.QStandardItem(str(value)) for value in row]
                    pc_model.appendRow(items)

                self.PC_TABLE.setModel(pc_model)
                self.PC_TABLE.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

                cursor.close()
                connection.close()

                if not filtered_results:
                    QMessageBox.information(self, "정보", "입력된 Probe Card ID와 일치하는 데이터가 없습니다.")
                    
                    # 빈 모델을 설정하여 테이블을 비웁니다.
                    empty_model = QtGui.QStandardItemModel()
                    empty_model.setHorizontalHeaderLabels(["PC_ID", "PC_GROUP", "설비", "위치", "TOTAL_SHOT"])
                    self.PC_TABLE.setModel(empty_model)
                    
                    # Main_tab으로 이동
                    QTimer.singleShot(0, self.switchToMainTab)  # QTimer를 사용하여 Main_tab으로 이동
                    return False

                return True
            else:
                QMessageBox.warning(self, "경고", "Probe Card 입력이 취소되었습니다.")
                
                # Main_tab으로 이동
                QTimer.singleShot(0, self.switchToMainTab)  # QTimer를 사용하여 Main_tab으로 이동
                return False

        except Exception as e:
            QMessageBox.critical(self, "에러", f"예외가 발생했습니다: {str(e)}")
            QTimer.singleShot(0, self.switchToMainTab)  # QTimer를 사용하여 Main_tab으로 이동
            return False


    def updatePIBTable(self):
        try:
            # LOT_TABLE에서 선택된 LOT_ID의 PRODUCT 값을 가져옵니다.
            lot_model = self.LOT_TABLE.model()
            if lot_model is None or self.selected_lot is None:
                QtWidgets.QMessageBox.warning(self, "경고", "LOT_TABLE에서 항목을 선택해주세요.")
                return

            product = lot_model.data(lot_model.index(self.selected_lot, 0))  # PRODUCT 컬럼의 값을 가져옵니다.
            product_prefix = product[:7]  # 앞자리 7자리를 추출합니다.

            dsn_tns = cx_Oracle.makedsn('192.168.222.113', 1521, service_name='fdryeds')
            connection = cx_Oracle.connect(user='Ark_select_user', password='ark12$select', dsn=dsn_tns)
            cursor = connection.cursor()

            query = """
            SELECT
                A.PC_ID AS PIB_ID,
                A.EQP_GROUP AS 설비,
                A.PARA
            FROM EDS_DB.PMS_MAIN A
                WHERE SUBSTR(A.OWNER_PC_ID, 2, 7) = :product_prefix
                
            """

            cursor.execute(query, {'product_prefix': product_prefix})
            results = cursor.fetchall()

            pib_model = QtGui.QStandardItemModel()
            pib_model.setHorizontalHeaderLabels(["PIB_ID", "설비", "PARA"])
            for row in results:
                items = [QtGui.QStandardItem(str(value)) for value in row]
                pib_model.appendRow(items)

            self.PIB_TABLE.setModel(pib_model)
            self.PIB_TABLE.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

            cursor.close()
            connection.close()

            if not results:
                # 결과가 없을 경우 수동 입력 팝업창 표시
                dialog = QDialog(self)
                dialog.setWindowTitle("PIB 수동 입력")
                dialog.resize(400, 250)
                layout = QVBoxLayout()

                # 스타일 시트 설정
                dialog.setStyleSheet("""
                    QDialog {
                        background-color: #f0f0f0;
                        border: 1px solid #c0c0c0;
                        border-radius: 10px;
                    }
                    QLabel {
                        font-size: 14pt;
                        font-weight: bold;
                        color: #333333;
                    }
                    QLineEdit {
                        font-size: 12pt;
                        padding: 5px;
                        border: 1px solid #c0c0c0;
                        border-radius: 5px;
                    }
                    QDialogButtonBox {
                        font-size: 12pt;
                    }
                    QPushButton {
                        background-color: #4CAF50;
                        color: white;
                        border: none;
                        padding: 10px 20px;
                        text-align: center;
                        text-decoration: none;
                        display: inline-block;
                        font-size: 12pt;
                        margin: 4px 2px;
                        border-radius: 5px;
                    }
                    QPushButton:hover {
                        background-color: #45a049;
                    }
                    QPushButton:pressed {
                        background-color: #3e8e41;
                    }
                """)

                # 안내 메시지
                message_label = QLabel("PIB 관련 쿼리에서 테이블 값이 없으면\nPIB를 수동으로 입력해주시기 바랍니다")
                layout.addWidget(message_label)

                # 입력 필드와 버튼 추가
                pib_id_label = QLabel("PIB_ID:")
                pib_id_input = QLineEdit()
                layout.addWidget(pib_id_label)
                layout.addWidget(pib_id_input)

                equipment_label = QLabel("설비:")
                equipment_input = QLineEdit()
                layout.addWidget(equipment_label)
                layout.addWidget(equipment_input)

                para_label = QLabel("PARA:")
                para_input = QLineEdit()
                layout.addWidget(para_label)
                layout.addWidget(para_input)

                button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel)
                button_box.accepted.connect(dialog.accept)
                button_box.rejected.connect(dialog.reject)
                layout.addWidget(button_box)

                dialog.setLayout(layout)

                # 팝업창 실행
                if dialog.exec_() == QDialog.Accepted:
                    pib_id = pib_id_input.text()
                    equipment = equipment_input.text()
                    para = para_input.text()

                    if not pib_id or not equipment or not para:
                        QMessageBox.warning(self, "경고", "모든 필드를 입력해주세요.")
                        empty_model = QtGui.QStandardItemModel()
                        empty_model.setHorizontalHeaderLabels(["PIB_ID", "설비", "PARA"])
                        self.PIB_TABLE.setModel(empty_model)
                        return

                    # PIB_ID 형식 검증: "-숫자3자리"로 끝나야 함
                    import re
                    if not re.match(r'.*-\d{3}$', pib_id):
                        QMessageBox.warning(self, "경고", "PIB_ID는 '-숫자3자리' 형식으로 끝나야 합니다.\n예: ABC-123")
                        empty_model = QtGui.QStandardItemModel()
                        empty_model.setHorizontalHeaderLabels(["PIB_ID", "설비", "PARA"])
                        self.PIB_TABLE.setModel(empty_model)
                        return

                    # 수동 입력된 데이터를 PIB_TABLE에 표시
                    manual_model = QtGui.QStandardItemModel()
                    manual_model.setHorizontalHeaderLabels(["PIB_ID", "설비", "PARA"])
                    items = [QtGui.QStandardItem(pib_id), QtGui.QStandardItem(equipment), QtGui.QStandardItem(para)]
                    manual_model.appendRow(items)
                    self.PIB_TABLE.setModel(manual_model)
                    self.PIB_TABLE.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)
                else:
                    # 취소된 경우 빈 테이블 표시
                    empty_model = QtGui.QStandardItemModel()
                    empty_model.setHorizontalHeaderLabels(["PIB_ID", "설비", "PARA"])
                    self.PIB_TABLE.setModel(empty_model)
        except Exception as e:
            # 예외가 발생하면 에러 메시지를 표시하고 프로그램이 종료되지 않도록 합니다.
            QMessageBox.critical(self, "에러", f"예외가 발생했습니다: {str(e)}")


    def onLotTableClicked(self, index):
        self.selected_lot = index.row()
        

    def onPCTableClicked(self, index):
        self.selected_pc = index.row()

    def onPIBTableClicked(self, index):
        self.selected_pib = index.row()
            
    def onInsertButtonClicked(self):
        # UTC59~UTC73 장비는 PIB 선택을 건너뛸 수 있음
        if self.skip_pib:
            if self.selected_lot is None or self.selected_pc is None:
                QtWidgets.QMessageBox.warning(self, "경고", "LOT과 PC 항목을 선택해주세요.")
                return
        else:
            # 일반 장비는 모든 테이블 선택 필요
            if self.selected_lot is None or self.selected_pc is None or self.selected_pib is None:
                QtWidgets.QMessageBox.warning(self, "경고", "모든 테이블에서 항목을 선택해주세요.")
                return

        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("사용자 정보 입력")
        layout = QtWidgets.QVBoxLayout()

        # 스타일 시트 설정
        dialog.setStyleSheet("""
            QDialog {
            background-color: #2e2e2e;
            border: 1px solid #1e1e1e;
            border-radius: 10px;
            }
            QLabel {
            font-size: 14pt;
            font-weight: bold;
            color: #f0f0f0;
            }
            QLineEdit, QTextEdit {
            font-size: 12pt;
            padding: 5px;
            border: 1px solid #1e1e1e;
            border-radius: 5px;
            background-color: #3e3e3e;
            color: #f0f0f0;
            }
            QDialogButtonBox {
            font-size: 12pt;
            }
            QPushButton {
            background-color: #4CAF50;
            color: white;
            border: none;
            padding: 10px 20px;
            text-align: center;
            text-decoration: none;
            display: inline-block;
            font-size: 12pt;
            margin: 4px 2px;
            border-radius: 5px;
            box-shadow: 3px 3px 5px #1e1e1e;
            }
            QPushButton:hover {
            background-color: #45a049;
            }
            QPushButton:pressed {
            background-color: #3e8e41;
            }
        """)

        user_id_label = QtWidgets.QLabel("USER_ID:")
        user_id_input = QtWidgets.QLineEdit()
        layout.addWidget(user_id_label)
        layout.addWidget(user_id_input)

        comment_label = QtWidgets.QLabel("COMMENT:")
        comment_input = QtWidgets.QTextEdit()
        layout.addWidget(comment_label)
        layout.addWidget(comment_input)

        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)
        
        # 'OK' 버튼 비활성화
        ok_button = button_box.button(QtWidgets.QDialogButtonBox.Ok)
        ok_button.setEnabled(False)
        ok_button.setStyleSheet("background-color: gray; color: white;")

        # 입력값 유효성 검사
        def validate_user_id(text):
            if text.isdigit() and len(text) == 8:
                ok_button.setEnabled(True)
                ok_button.setStyleSheet("background-color: #4CAF50; color: white;")  # 활성화 시 초록색
            else:
                ok_button.setEnabled(False)
                ok_button.setStyleSheet("background-color: gray; color: white;")  # 비활성화 시 회색

        user_id_input.textChanged.connect(validate_user_id)

        def validate_user_id(text):
            if text.isdigit() and len(text) == 8:
                ok_button.setEnabled(True)
            else:
                ok_button.setEnabled(False)

        user_id_input.textChanged.connect(validate_user_id)

        dialog.setLayout(layout)

        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            user_id = user_id_input.text()
            comment = comment_input.toPlainText()
            
            # Update all textBrowser widgets
            lot_model = self.LOT_TABLE.model()
            if lot_model and self.selected_lot is not None:
                product = lot_model.data(lot_model.index(self.selected_lot, 0))  # PRODUCT 컬럼의 값을 가져옵니다.
                self.textBrowser.setText(product)  # textBrowser에 PRODUCT 값을 설정합니다

            self.textBrowser_2.setText(self.LOT_TABLE.model().data(self.LOT_TABLE.model().index(self.selected_lot, 2)))
            self.textBrowser_3.setText(self.LOT_TABLE.model().data(self.LOT_TABLE.model().index(self.selected_lot, 1)))
            self.textBrowser_4.setText(self.PC_TABLE.model().data(self.PC_TABLE.model().index(self.selected_pc, 0)))
            
            # PIB 처리: UTC59~UTC73 장비면 빈 문자열, 아니면 선택된 PIB 값
            if self.skip_pib:
                self.textBrowser_5.setText("")  # PIB_ID는 빈 값으로 설정
            else:
                self.textBrowser_5.setText(self.PIB_TABLE.model().data(self.PIB_TABLE.model().index(self.selected_pib, 0)))
            
            self.textBrowser_6.setText(user_id)
            self.textBrowser_7.setText(comment)

            print(f"USER_ID: {user_id}")
            print(f"COMMENT: {comment}")
            self.closeAllViews()
            
            # 데이터가 정상적으로 추출되었다고 가정하고 Monitor 탭으로 이동
            self.switchToMonitorTab()
        else:
            QtWidgets.QMessageBox.warning(self, "경고", "사번을 입력해주세요(8자리_숫자)")
    
    def insertDataToInsertList(self):
        if self.INSERT_LIST:
            row_position = self.INSERT_LIST.rowCount()
            self.INSERT_LIST.insertRow(row_position)

            # DEVICE (PRODUCT) 데이터 추가
            device_item = QtWidgets.QTableWidgetItem(self.selected_product)
            self.INSERT_LIST.setItem(row_position, 0, device_item)

            # LOT_ID 데이터 추가
            lot_model = self.LOT_TABLE.model()
            if lot_model and self.selected_lot is not None:
                lot_id = lot_model.data(lot_model.index(self.selected_lot, 1))
                lot_item = QtWidgets.QTableWidgetItem(str(lot_id))
                self.INSERT_LIST.setItem(row_position, 1, lot_item)

            # STEP_ID (STEP_SEQ) 데이터 추가
            if lot_model and self.selected_lot is not None:
                step_seq = lot_model.data(lot_model.index(self.selected_lot, 0))
                step_item = QtWidgets.QTableWidgetItem(str(step_seq))
                self.INSERT_LIST.setItem(row_position, 2, step_item)

            # PC_ID (PC_NO) 데이터 추가
            pc_model = self.PC_TABLE.model()
            if pc_model and self.selected_pc is not None:
                pc_no = pc_model.data(pc_model.index(self.selected_pc, 0))
                pc_item = QtWidgets.QTableWidgetItem(str(pc_no))
                self.INSERT_LIST.setItem(row_position, 3, pc_item)

            # PB_ID (PC_ID from PIB_TABLE) 데이터 추가
            pib_model = self.PIB_TABLE.model()
            if pib_model and self.selected_pib is not None:
                pb_id = pib_model.data(pib_model.index(self.selected_pib, 0))
                pb_item = QtWidgets.QTableWidgetItem(str(pb_id))
                self.INSERT_LIST.setItem(row_position, 4, pb_item)

            self.INSERT_LIST.resizeColumnsToContents()
            self.INSERT_LIST.resizeRowsToContents()
        else:
            print("INSERT_LIST widget not found")

    def closeAllViews(self):
        if self.grid_layout_2_widget:
            self.grid_layout_2_widget.hide()
        self.tableWidget.hide()
    
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.loading_overlay.setGeometry(self.rect())
        if self.tableWidget.isVisible():
            self.tableWidget.setGeometry(50, 90, self.width() - 100, self.height() - 190)
            # 필터 위젯 크기 조정
            if hasattr(self, 'filter_widget'):
                self.filter_widget.setGeometry(50, 50, self.width() - 100, 40)
            # Close 버튼을 테이블 오른쪽 하단에 붙여서 일체감 연출
            table_right = 50 + (self.width() - 100)  # 테이블 오른쪽 끝
            table_bottom = 90 + (self.height() - 190)  # 테이블 아래쪽 끝
            self.closeTableButton.setGeometry(table_right - 120, table_bottom - 1, 120, 30)
            self.closeTableButton.show()
        else:
            self.closeTableButton.hide()

    def closeMainWindow(self):
        self.close()
    
    def insert_data(self):
        try:
            # 데이터 가져오기
            eqp_id = self.EQP_ID.text()  # QLineEdit는 text() 사용
            device = self.textBrowser.toPlainText()
            lot_id = self.textBrowser_2.toPlainText()
            step_id = self.textBrowser_3.toPlainText()
            pc_id = self.textBrowser_4.toPlainText()
            pb_id = self.textBrowser_5.toPlainText() if self.textBrowser_5.toPlainText() else None  # 빈 값이면 None으로 처리
            user_id = int(self.textBrowser_6.toPlainText())
            status_id = self.STATUS_ID.text()
            
            current_time = datetime.now()
            local_ip = socket.gethostbyname(socket.gethostname())

            # Oracle DB 연결
            dsn_tns = cx_Oracle.makedsn('192.168.223.13', 1521, service_name='ERPSIMAX')
            conn = cx_Oracle.connect(user='RPA', password='rpa01!', dsn=dsn_tns)
            cursor = conn.cursor()

            # 테이블명 수정 및 데이터 삽입
            cursor.execute("""
                INSERT INTO RPA_ADMIN.interface 
                (EQPID, DATE_, DEVICE, LOT_ID, STEP_ID, PC_ID, PB_ID, USER_ID, IP, STATUS)
                VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9, :10)
            """, (eqp_id, current_time, device, lot_id, step_id, pc_id, pb_id, user_id, local_ip, status_id))
            
            conn.commit()
            cursor.close()
            conn.close()
            
            QtWidgets.QMessageBox.information(self, "성공", "데이터가 성공적으로 저장되었습니다.")
            
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            QtWidgets.QMessageBox.critical(self, "오류", f"데이터베이스 오류: {error.message}")
    # 수정전
    # def showUserInputDialog(self, eqp_id):
    #     dialog = QtWidgets.QDialog(self)
    #     dialog.setWindowTitle("사용자 정보 입력")
    #     layout = QtWidgets.QVBoxLayout()

    #     user_id_label = QtWidgets.QLabel("USER_ID:")
    #     user_id_input = QtWidgets.QLineEdit()
    #     layout.addWidget(user_id_label)
    #     layout.addWidget(user_id_input)

    #     button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
    #     button_box.accepted.connect(dialog.accept)
    #     button_box.rejected.connect(dialog.reject)
    #     layout.addWidget(button_box)

    #     ok_button = button_box.button(QtWidgets.QDialogButtonBox.Ok)
    #     ok_button.setEnabled(False)

    #     def validate_user_id(text):
    #         if text.isdigit() and len(text) == 8:
    #             ok_button.setEnabled(True)
    #         else:
    #             ok_button.setEnabled(False)

    #     user_id_input.textChanged.connect(validate_user_id)

    #     dialog.setLayout(layout)

    #     if dialog.exec_() == QtWidgets.QDialog.Accepted:
    #         user_id = user_id_input.text()
    #         self.updateMonitoringTab(eqp_id, user_id)
    #     else:
    #         QtWidgets.QMessageBox.warning(self, "경고", "사번을 입력해주세요(8자리_숫자)")
    # 수정중
    def showUserInputDialog(self, eqp_id):
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("사용자 정보 입력")
        layout = QtWidgets.QVBoxLayout()

        user_id_label = QtWidgets.QLabel("USER_ID:")
        user_id_input = QtWidgets.QLineEdit()
        layout.addWidget(user_id_label)
        layout.addWidget(user_id_input)

        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        button_box.accepted.connect(lambda: self.validateAndProceed(dialog, user_id_input.text(), eqp_id))
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        ok_button = button_box.button(QtWidgets.QDialogButtonBox.Ok)
        ok_button.setEnabled(False)

        # 입력값 유효성 검사
        def validate_user_id(text):
            if text.isdigit() and len(text) == 8:  # USER_ID는 8자리 숫자여야 함
                ok_button.setEnabled(True)
            else:
                ok_button.setEnabled(False)

        user_id_input.textChanged.connect(validate_user_id)

        dialog.setLayout(layout)
        dialog.exec_()

    def validateAndProceed(self, dialog, user_id, eqp_id):
        try:
            # DB 연결
            dsn = cx_Oracle.makedsn("mes.nepes.co.kr", 1521, "CCUBE")
            connection = cx_Oracle.connect("mighty", "mighty", dsn)
            cursor = connection.cursor()
    
            # 쿼리 실행
            query = """
                SELECT USER_ID
                FROM userinfo
                WHERE gw_dept_name LIKE '%하이퍼%'
            """
            cursor.execute(query)
            results = cursor.fetchall()
    
            # 디버깅용 출력
            print("Query Results:", results)
    
            # 입력된 USER_ID가 결과에 있는지 확인
            valid_user_ids = [str(row[0]).strip() for row in results]  # USER_ID가 첫 번째 컬럼에 있다고 가정
            print("Valid User IDs:", valid_user_ids)
    
            if user_id.strip() in valid_user_ids:
                print("Valid USER_ID:", user_id)
                self.updateMonitoringTab(eqp_id, user_id)
                dialog.accept()  # 팝업창 닫기
            else:
                print("Invalid USER_ID:", user_id)
                QtWidgets.QMessageBox.warning(self, "경고", "승인되지 않은 사용자입니다.")
                return  # 동작 중단
        except cx_Oracle.DatabaseError as e:
            error, = e.args
            print("Database error:", error.message)
            QtWidgets.QMessageBox.critical(self, "오류", f"데이터베이스 오류: {error.message}")
        finally:
            cursor.close()
            connection.close()
            
    def showUserAndKeyDialog(self):
        # 새로운 팝업창 생성
        dialog = QtWidgets.QDialog(self)
        dialog.setWindowTitle("사용자 정보 및 등록KEY 입력")
        layout = QtWidgets.QVBoxLayout()

        # 스타일 시트 설정
        dialog.setStyleSheet("""
            QDialog {
                background-color: #2e2e2e;
                border: 1px solid #1e1e1e;
                border-radius: 10px;
                box-shadow: 5px 5px 15px rgba(0, 0, 0, 0.5);
            }
            QLabel {
                font-size: 14pt;
                font-weight: bold;
                color: #f0f0f0;
            }
            QLineEdit {
                font-size: 12pt;
                padding: 8px;
                border: 1px solid #1e1e1e;
                border-radius: 5px;
                background-color: #3e3e3e;
                color: #f0f0f0;
                box-shadow: inset 2px 2px 5px rgba(0, 0, 0, 0.3);
            }
            QDialogButtonBox {
                font-size: 12pt;
            }
            QPushButton {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                text-align: center;
                text-decoration: none;
                display: inline-block;
                font-size: 12pt;
                margin: 4px 2px;
                border-radius: 5px;
                box-shadow: 3px 3px 5px rgba(0, 0, 0, 0.3);
            }
            QPushButton:hover {
                background-color: #45a049;
            }
            QPushButton:pressed {
                background-color: #3e8e41;
                box-shadow: inset 2px 2px 5px rgba(0, 0, 0, 0.3);
            }
        """)

        # USER_ID 입력 필드
        user_id_label = QtWidgets.QLabel("USER_ID:")
        user_id_input = QtWidgets.QLineEdit()
        layout.addWidget(user_id_label)
        layout.addWidget(user_id_input)

        # 등록KEY 입력 필드
        key_label = QtWidgets.QLabel("등록KEY:")
        key_input = QtWidgets.QLineEdit()
        layout.addWidget(key_label)
        layout.addWidget(key_input)

        # 버튼 박스 추가
        button_box = QtWidgets.QDialogButtonBox(QtWidgets.QDialogButtonBox.Ok | QtWidgets.QDialogButtonBox.Cancel)
        button_box.accepted.connect(dialog.accept)
        button_box.rejected.connect(dialog.reject)
        layout.addWidget(button_box)

        # 'OK' 버튼 비활성화
        ok_button = button_box.button(QtWidgets.QDialogButtonBox.Ok)
        ok_button.setEnabled(False)

        # 입력값 유효성 검사
        def validate_inputs():
            if user_id_input.text().isdigit() and len(user_id_input.text()) == 8 and key_input.text():
                ok_button.setEnabled(True)
            else:
                ok_button.setEnabled(False)

        user_id_input.textChanged.connect(validate_inputs)
        key_input.textChanged.connect(validate_inputs)

        dialog.setLayout(layout)

        # 팝업창 실행
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            user_id = user_id_input.text()
            reg_key = key_input.text()
            QtWidgets.QMessageBox.information(self, "입력 완료", f"USER_ID: {user_id}\n등록KEY: {reg_key}")
        else:
            QtWidgets.QMessageBox.warning(self, "취소", "사용자 정보 입력이 취소되었습니다.")

    def updateMonitoringTab(self, eqp_id, user_id):
        self.textBrowser.setText(eqp_id)
        self.textBrowser_2.setText("")
        self.textBrowser_3.setText("") 
        self.textBrowser_4.setText("")
        self.textBrowser_5.setText("")
        self.textBrowser_6.setText(user_id)
        self.textBrowser_7.setText("")
        self.switchToMonitorTab()


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    window = MyWindow()
    window.show()   
    sys.exit(app.exec_())

