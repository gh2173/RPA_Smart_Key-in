# Campus Selection Modifications for RPA Smart Key-in Manager
# This file contains the required functions to be integrated into the Jupyter notebook

from PyQt5.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QRadioButton, QButtonGroup, QPushButton, QLabel, QMessageBox
from PyQt5.QtCore import Qt

class CampusSelectionDialog(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("캠퍼스 선택")
        self.setModal(True)
        self.setFixedSize(300, 150)
        
        # Create layout
        layout = QVBoxLayout()
        
        # Title label
        title_label = QLabel("캠퍼스를 선택하세요:")
        layout.addWidget(title_label)
        
        # Radio buttons for campus selection
        radio_layout = QHBoxLayout()
        self.button_group = QButtonGroup()
        
        self.ns2_radio = QRadioButton("NS2")
        self.ns3_radio = QRadioButton("NS3")
        
        self.button_group.addButton(self.ns2_radio, 1)
        self.button_group.addButton(self.ns3_radio, 2)
        
        radio_layout.addWidget(self.ns2_radio)
        radio_layout.addWidget(self.ns3_radio)
        layout.addLayout(radio_layout)
        
        # OK/Cancel buttons
        button_layout = QHBoxLayout()
        self.ok_button = QPushButton("OK")
        self.cancel_button = QPushButton("Cancel")
        
        button_layout.addWidget(self.ok_button)
        button_layout.addWidget(self.cancel_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
        # Connect signals
        self.ok_button.clicked.connect(self.accept)
        self.cancel_button.clicked.connect(self.reject)
        
        self.selected_campus = None
    
    def accept(self):
        # Check if a campus is selected
        if not self.button_group.checkedButton():
            QMessageBox.warning(self, "경고", "캠퍼스를 선택해주세요.")
            return
        
        # Get selected campus
        if self.ns2_radio.isChecked():
            self.selected_campus = "NS2"
        elif self.ns3_radio.isChecked():
            self.selected_campus = "NS3"
        
        super().accept()
    
    def get_selected_campus(self):
        return self.selected_campus


# Functions to be added to MyWindow class:

def showCampusSelectionDialog(self, action_type):
    """
    Show campus selection dialog and proceed based on user selection
    """
    dialog = CampusSelectionDialog(self)
    result = dialog.exec_()
    
    if result == QDialog.Accepted:
        campus = dialog.get_selected_campus()
        if campus:
            self.showTableWithCampus(action_type, campus)

def showTable(self, action_type):
    """
    Modified showTable function that calls campus selection dialog
    """
    self.showCampusSelectionDialog(action_type)

def showTableWithCampus(self, action_type, campus):
    """
    Original showTable logic with campus parameter
    """
    self.current_action = action_type  # 현재 액션 저장
    self.current_campus = campus  # 선택된 캠퍼스 저장
    
    # Update STATUS_ID to show both action_type and campus
    status_text = f"{action_type} - {campus}"
    self.STATUS_ID.setText(status_text)  # Monitor 탭의 STATUS_ID에 텍스트 설정
    
    self.loading_overlay.setGeometry(self.rect())
    self.loading_overlay.show()
    QTimer.singleShot(100, self.executeQuery)
    self.closeTableButton.show()

def executeQuery(self):
    """
    Modified executeQuery function that filters by selected campus
    """
    # 데이터베이스 연결 정보 수정
    dsn = cx_Oracle.makedsn("mes.nepes.co.kr", 1521, "CCUBE")
    connection = cx_Oracle.connect("mighty", "mighty", dsn)
    cursor = connection.cursor()

    # Original query with campus filter added
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
                /* 기타 등 등: NULL 반환 */
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
        AND x.CAMPUS = :campus
        """
    
    # Execute query with campus parameter
    campus_param = getattr(self, 'current_campus', None)
    if not campus_param:
        # Fallback if current_campus is not set
        campus_param = 'NS2'  # Default to NS2
    
    cursor.execute(query, {'campus': campus_param})
    results = sorted(cursor.fetchall(), key=lambda x: x[2] if x[2] is not None else '')

    # Rest of the original executeQuery function logic continues here...
    # (The actual table population logic would follow)
    
    cursor.close()
    connection.close()


# Instructions for integration into MyWindow class __init__ method:
"""
Add this line to the __init__ method after self.setupUi(self):

    self.current_campus = None  # Initialize campus selection
"""