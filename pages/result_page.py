from PyQt5.QtWidgets import QVBoxLayout, QLabel, QWidget, QGridLayout, QPushButton
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtCore import Qt
import cv2
class ResultPage(QWidget):

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.results_layout = QGridLayout()
        self.layout.addLayout(self.results_layout)

        self.back_button = QPushButton("Back to Start Page")
        self.layout.addWidget(self.back_button)

        self.setLayout(self.layout)



    def clear_results_layout(self):
        while self.results_layout.count():
            item = self.results_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def set_prediction_results(self, age_predictions, gender_predictions, detected_faces):
        self.clear_results_layout()

        row = 1
        for face_id, face_img in detected_faces.items():
            gender = gender_predictions[face_id]
            age = age_predictions[face_id]
            gender_text = 'Male' if gender == 0 else 'Female'

            # 이미지 크기 조정: 얼굴 크기에 따라 적절한 크기로 조정
            height, width, _ = face_img.shape
            scale_factor = min(100 / width, 100 / height)  # 100x100 크기로 조정
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            face_img = cv2.resize(face_img, (new_width, new_height))

            img_label = QLabel(self)
            img_label.setAlignment(Qt.AlignCenter)
            face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
            height, width, channel = face_img.shape
            bytes_per_line = 3 * width
            q_img = QImage(face_img.data, width, height, bytes_per_line, QImage.Format_RGB888)
            img_label.setPixmap(QPixmap.fromImage(q_img).scaled(100, 100, Qt.KeepAspectRatio))

            text_label = QLabel(f"{row}. Face_id: {face_id} Age: {age}, Gender: {gender_text}")
            text_label.setAlignment(Qt.AlignCenter)

            self.results_layout.addWidget(img_label, row, 0)
            self.results_layout.addWidget(text_label, row, 1)
            row += 1

