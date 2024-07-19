from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtGui import QPainter, QColor, QBrush, QPixmap, QPen, QFont
from PyQt5.QtCore import Qt, QRectF


class AmusementParkPage(QWidget):
    def __init__(self, recommendation_res=[]):
        super().__init__()

        self.text_space=300
        self.recommendation_res = recommendation_res
        
        self.layout = QVBoxLayout()
        
        self.text_label = QLabel("Test", self)
        self.text_label.setAlignment(Qt.AlignCenter)
        self.text_label.setStyleSheet("font-size: 15px; font-weight: bold;")
        self.text_label.setMinimumHeight(100)  # Adjust the height as needed
        self.layout.addWidget(self.text_label)
        self.layout.addStretch()

        # Display background image using QLabel
        self.background_label = QLabel(self)
        self.background_image = QPixmap('../ui_images/park.png') 
        self.background_label.setPixmap(self.background_image)
        self.background_label.setScaledContents(True)
        self.layout.addWidget(self.background_label)
        self.layout.addStretch()

        self.back_button = QPushButton("Back to Start Page")
        self.layout.addWidget(self.back_button, alignment=Qt.AlignBottom | Qt.AlignCenter)
        
        self.setLayout(self.layout)
    
