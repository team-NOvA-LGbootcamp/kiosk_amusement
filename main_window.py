import sys
import cv2  # cv2 모듈 추가
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout
from PyQt5.QtGui import QPixmap, QImage
from camera_widget import CameraWidget

class SecondPage(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        
        self.results_layout = QGridLayout()
        self.layout.addLayout(self.results_layout)

        self.button = QPushButton("Back to First Page")
        self.button.clicked.connect(self.back_to_first_page)
        self.layout.addWidget(self.button)
        
        self.setLayout(self.layout)
    
    def set_prediction_results(self, age_predictions, gender_predictions, detected_faces):
        self.clear_results_layout()
        for i, (age, gender, face_img) in enumerate(zip(age_predictions, gender_predictions, detected_faces)):
            gender_text = 'Male' if gender == 0 else 'Female'
            
            img_label = QLabel(self)
            img_label.setAlignment(Qt.AlignCenter)
            face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
            height, width, channel = face_img.shape
            bytes_per_line = 3 * width
            q_img = QImage(face_img.data, width, height, bytes_per_line, QImage.Format_RGB888)
            img_label.setPixmap(QPixmap.fromImage(q_img).scaled(100, 100, Qt.KeepAspectRatio))

            text_label = QLabel(f"Age: {age}, Gender: {gender_text}")
            text_label.setAlignment(Qt.AlignCenter)

            self.results_layout.addWidget(img_label, i, 0)
            self.results_layout.addWidget(text_label, i, 1)
    
    def clear_results_layout(self):
        while self.results_layout.count():
            item = self.results_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def back_to_first_page(self):
        self.parentWidget().setCurrentIndex(0)
        self.parentWidget().widget(0).start_webcam()

class MainWindow(QMainWindow):
    def __init__(self, model):
        super().__init__()

        self.model = model

        # QStackedWidget 생성
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # 첫 번째 페이지 생성 및 추가
        self.first_page = CameraWidget()
        self.stacked_widget.addWidget(self.first_page)

        # 두 번째 페이지 생성 및 추가
        self.second_page = SecondPage()
        self.stacked_widget.addWidget(self.second_page)

        # 윈도우 설정
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 540, 960)
        self.setFixedSize(540, 960)

        # CameraWidget의 switch_page 신호와 페이지 전환 연결
        self.first_page.switch_page.connect(self.show_second_page)

    def show_second_page(self, detected_faces):
        self.first_page.stop_webcam()  # 웹캠 정지
        age_predictions, gender_predictions = self.model.predict_image(detected_faces)
        self.second_page.set_prediction_results(age_predictions, gender_predictions, detected_faces)
        self.stacked_widget.setCurrentWidget(self.second_page)
