# Campus Selection Integration Instructions

Due to limitations with the Jupyter notebook editing tools, please follow these manual integration steps to add the campus selection functionality to your RPA Smart Key-in Manager notebook.

## Files Created
- `campus_selection_modifications.py` - Contains all the new code components
- `INTEGRATION_INSTRUCTIONS.md` - This instruction file

## Step 1: Update Imports

In the first code cell of your Jupyter notebook, find this line:
```python
from PyQt5.QtWidgets import QPushButton, QGraphicsDropShadowEffect, QProgressDialog
```

Replace it with:
```python
from PyQt5.QtWidgets import QPushButton, QGraphicsDropShadowEffect, QProgressDialog, QButtonGroup, QRadioButton, QHBoxLayout
```

## Step 2: Initialize current_campus Attribute

In the `MyWindow` class `__init__` method, right after the line:
```python
self.setupUi(self)
```

Add this line:
```python
self.current_campus = None  # Initialize campus selection
```

## Step 3: Add the Campus Selection Dialog Class

Add the following class definition in a new code cell (preferably before the MyWindow class):

```python
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
```

## Step 4: Add the showCampusSelectionDialog Method

Add this method to the `MyWindow` class:

```python
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
```

## Step 5: Modify the Existing showTable Method

Find the existing `showTable` method:
```python
def showTable(self, action_type):
    self.current_action = action_type  # 현재 액션 저장
    self.STATUS_ID.setText(action_type)  # Monitor 탭의 STATUS_ID에 텍스트 설정
    self.loading_overlay.setGeometry(self.rect())
    self.loading_overlay.show()
    QTimer.singleShot(100, self.executeQuery)
    self.closeTableButton.show()
```

Replace it with:
```python
def showTable(self, action_type):
    """
    Modified showTable function that calls campus selection dialog
    """
    self.showCampusSelectionDialog(action_type)
```

## Step 6: Add the showTableWithCampus Method

Add this new method to the `MyWindow` class:

```python
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
```

## Step 7: Modify the executeQuery Method

In the `executeQuery` method, find this section:
```python
WHERE x.CAMPUS IS NOT NULL
AND x.PLANT IN 'CCUBEDIGITAL'
AND x.MAIN_STATUS NOT IN ('RUN', 'SHUTDOWN')
```

Replace it with:
```python
WHERE x.CAMPUS IS NOT NULL
AND x.PLANT IN 'CCUBEDIGITAL'
AND x.MAIN_STATUS NOT IN ('RUN', 'SHUTDOWN')
AND x.CAMPUS = :campus
```

Then, find the line:
```python
cursor.execute(query)
```

Replace it with:
```python
# Get the selected campus, default to NS2 if not set
campus_param = getattr(self, 'current_campus', 'NS2')
cursor.execute(query, {'campus': campus_param})
```

## Testing the Implementation

After making these changes:

1. Restart the Jupyter kernel
2. Run all cells
3. When you click on any action button (like "IDLE OVER 2HR"), you should see:
   - A campus selection dialog with "NS2" and "NS3" radio buttons
   - Warning message if no campus is selected when clicking OK
   - The STATUS_ID should show both the action type and selected campus (e.g., "IDLE OVER 2HR - NS2")
   - The data table should be filtered to show only equipment from the selected campus

## Troubleshooting

- If you get import errors, make sure all the new imports are added correctly
- If the dialog doesn't show, check that the CampusSelectionDialog class is defined before the MyWindow class
- If filtering doesn't work, verify that the query modification and parameter binding are correct
- Check the console for any error messages during execution

## File Locations

All modification files are saved in:
- `/Users/gh_mac-book/Desktop/PROJECT_GH/RPA_Smart_Key-in/campus_selection_modifications.py`
- `/Users/gh_mac-book/Desktop/PROJECT_GH/RPA_Smart_Key-in/INTEGRATION_INSTRUCTIONS.md`