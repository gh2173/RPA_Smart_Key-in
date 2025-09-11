"""
로딩 오버레이 위젯 모듈
"""

from PyQt5.QtWidgets import QLabel
from PyQt5.QtCore import QTimer, Qt
from PyQt5.QtGui import QPainter, QColor, QBrush
import math


class LoadingOverlay(QLabel):
    """로딩 화면을 표시하는 오버레이 위젯"""
    
    def __init__(self, parent=None):
        """
        LoadingOverlay 초기화
        
        Args:
            parent: 부모 위젯
        """
        super().__init__(parent)
        self.setFixedSize(100, 100)
        self.setStyleSheet("background-color: rgba(255, 255, 255, 200); border-radius: 10px;")
        self.setAttribute(Qt.WA_TranslucentBackground)
        
        self.angle = 0
        self.timer = QTimer()
        self.timer.timeout.connect(self.rotate)
        self.timer.start(50)
        
    def rotate(self):
        """회전 애니메이션 처리"""
        self.angle = (self.angle + 10) % 360
        self.update()
        
    def paintEvent(self, event):
        """그리기 이벤트 처리"""
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)
        
        painter.translate(self.width() / 2, self.height() / 2)
        painter.rotate(self.angle)
        
        for i in range(8):
            alpha = 255 - (i * 30)
            if alpha < 30:
                alpha = 30
            color = QColor(0, 0, 0, alpha)
            painter.setBrush(QBrush(color))
            painter.setPen(color)
            
            angle_rad = math.radians(i * 45)
            x = 25 * math.cos(angle_rad)
            y = 25 * math.sin(angle_rad)
            
            painter.drawEllipse(int(x) - 3, int(y) - 3, 6, 6)