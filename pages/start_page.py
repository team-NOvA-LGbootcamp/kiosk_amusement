from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt

class StartPage(QWidget):
    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()

        self.title_label = QLabel("DEMO", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setStyleSheet("font-size: 50px; font-weight: bold;")
        

        self.start_button = QPushButton("START", self)
        self.start_button.setStyleSheet("font-size: 24px;")
        self.start_button.clicked.connect(self.go_to_second_page)
        
        self.layout.addWidget(self.title_label)
        self.layout.addWidget(self.start_button)
        self.layout.setAlignment(Qt.AlignCenter)
        self.setLayout(self.layout)

    def go_to_second_page(self):
        self.parentWidget().setCurrentIndex(1)  # Switch to second page
