from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt

class StartPage(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()

        self.title_label = QLabel("DEMO", self)
        self.title_label.setObjectName("title_label")
        self.title_label.setAlignment(Qt.AlignCenter)
        

        self.start_button = QPushButton("START", self)
        self.start_button.setObjectName("start_button")
        
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.start_button)
        self.layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)

