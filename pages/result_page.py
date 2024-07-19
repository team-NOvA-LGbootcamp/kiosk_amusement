from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtCore import Qt
import cv2

class ResultPage(QWidget):
    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.results_layout = QGridLayout()
        self.layout.addLayout(self.results_layout)

        self.back_button = QPushButton("Back to Start Page")
        self.back_button.clicked.connect(self.back_to_start_page)
        self.layout.addWidget(self.back_button)

        self.setLayout(self.layout)

    def set_prediction_results(self, age_predictions, gender_predictions, detected_faces):
        self.clear_results_layout()
        for i, (age, gender, (face_id, face_imgs)) in enumerate(zip(age_predictions, gender_predictions, detected_faces.items())):
            gender_text = 'Male' if gender == 0 else 'Female'
            img_label = QLabel(self)
            img_label.setAlignment(Qt.AlignCenter)
            face_img = face_imgs[-1]
            face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
            height, width, channel = face_img.shape
            bytes_per_line = 3 * width
            q_img = QImage(face_img.data, width, height, bytes_per_line, QImage.Format_RGB888)
            img_label.setPixmap(QPixmap.fromImage(q_img).scaled(100, 100, Qt.KeepAspectRatio))

            text_label = QLabel(f"{i}. Face_id: {face_id} Age: {age}, Gender: {gender_text}")
            text_label.setAlignment(Qt.AlignCenter)

            self.results_layout.addWidget(img_label, i, 0)
            self.results_layout.addWidget(text_label, i, 1)

    def clear_results_layout(self):
        while self.results_layout.count():
            item = self.results_layout.takeAt(0)
            if item.widget():
                item.widget().deleteLater()

    def back_to_start_page(self):
        self.parentWidget().setCurrentIndex(0)  # Switch to start page
