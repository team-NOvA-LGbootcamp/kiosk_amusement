from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QImage, QPixmap, QIcon

class StartPage(QWidget):
    def __init__(self, icon_path):
        super().__init__()
        self.layout = QVBoxLayout()

        self.icon_label = QLabel()
        pixmap = QPixmap(icon_path)
        self.icon_label.setPixmap(pixmap.scaled(150,150,Qt.KeepAspectRatio, Qt.SmoothTransformation))
        self.icon_label.setAlignment(Qt.AlignCenter)

        self.title_label = QLabel("NAMU", self)
        self.title_label.setObjectName("title_label")
        self.title_label.setAlignment(Qt.AlignCenter)
        

        self.start_button = QPushButton("START", self)
        self.start_button.setObjectName("start_button")

        self.layout.addWidget(self.icon_label)        
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.start_button)
        self.layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)

