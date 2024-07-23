from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QIcon

class DevPage(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.title_label = QLabel("DEV_PAGE", self)
        self.title_label.setObjectName("title_label")
        self.title_label.setAlignment(Qt.AlignCenter)
        
        self.single_button = QPushButton("싱글 페이지로 가기", self)
        self.single_button.setObjectName("start_button")
        self.multi_button = QPushButton("2명 페이지로 가기", self)
        self.multi_button.setObjectName("start_button")
      
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.single_button)
        self.layout.addWidget(self.multi_button)
        self.layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)

