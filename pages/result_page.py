from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QWidget, QScrollArea, QPushButton, QSizePolicy
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtCore import Qt, pyqtSignal, QSize
import cv2

class MultiResultPage(QWidget):
    relation_clicked = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # 상단 레이아웃 (얼굴 사진 및 나이/성별 예측 결과)
        self.top_layout = QVBoxLayout()
        self.top_widget = QWidget()
        self.top_widget.setLayout(self.top_layout)
        self.top_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.layout.addWidget(self.top_widget)

        # 결과 레이아웃
        self.results_layout = QVBoxLayout()
        self.results_widget = QWidget()
        self.results_widget.setLayout(self.results_layout)
        
        # 스크롤 영역 (관계 예측 결과)
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.results_widget)
        self.layout.addWidget(self.scroll_area)

        # 뒤로가기 버튼
        self.back_button = QPushButton("Back to Start Page")
        self.back_button.setObjectName("back_button")
        self.layout.addWidget(self.back_button)

    def clear_all_layouts(self):
        # 상단 레이아웃 정리
        while self.top_layout.count():
            item = self.top_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

        # 결과 레이아웃 정리
        while self.results_layout.count():
            item = self.results_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

    def set_prediction_results(self, age_predictions, gender_predictions, detected_faces, relation_predictions):
        self.clear_all_layouts()

        # result_label = QLabel(self)
        # result_label.setAlignment(Qt.AlignCenter)
        # result_label.setObjectName("result_label")
        # result_label.setText("이렇게 함께 오신 것 같아요!")
        # self.top_layout.addWidget(result_label)

        # 얼굴 사진 및 나이/성별 예측 결과 추가
        face_list_widget = QWidget()
        face_list_layout = QHBoxLayout()
        for face_id, face_img in detected_faces.items():
            gender = gender_predictions[face_id]
            age = age_predictions[face_id]
            gender_text = '남자' if gender == 0 else '여자'

            # 이미지 크기 조정: 얼굴 크기에 따라 적절한 크기로 조정
            height, width, _ = face_img.shape
            scale_factor = min(50 / width, 50 / height)  # 크기를 절반으로 줄임
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            face_img = cv2.resize(face_img, (new_width, new_height))

            img_label = QLabel(self)
            img_label.setAlignment(Qt.AlignCenter)
            face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
            height, width, channel = face_img.shape
            bytes_per_line = 3 * width
            q_img = QImage(face_img.data, width, height, bytes_per_line, QImage.Format_RGB888)
            img_label.setPixmap(QPixmap.fromImage(q_img).scaled(50, 50, Qt.KeepAspectRatio))

            info_label = QLabel(f"나이: {age}<br>성별: {gender_text}")
            info_label.setAlignment(Qt.AlignCenter)
            info_label.setTextFormat(Qt.RichText)  # HTML 형식으로 설정

            face_layout = QVBoxLayout()
            face_layout.addWidget(img_label)
            face_layout.addWidget(info_label)

            face_list_layout.addLayout(face_layout)
        face_list_widget.setLayout(face_list_layout)
        self.top_layout.addWidget(face_list_widget)

        suggestion_label = QLabel(self)
        suggestion_label.setAlignment(Qt.AlignCenter)
        suggestion_label.setObjectName("suggestion_label")
        suggestion_label.setText("혹시 이렇게 오셨나요?")
        self.top_layout.addWidget(suggestion_label)
        
        # 관계 예측 결과 표시
        relation_icons = {
            'friend': 'icons/friend.png',
            'family': 'icons/family.png',
            'couple': 'icons/couple.png'
        }
        relation_labels = {'friend' : '친구', 'family' : '가족', 'couple' : '연인'}
        sorted_relations = sorted(relation_predictions.items(), key=lambda x: x[1], reverse=True)
        for relation, prob in sorted_relations:
            relation_button = QPushButton()
            relation_button.setObjectName("relation_button")

            # 아이콘 설정
            icon_path = relation_icons.get(relation, 'icons/default.png')
            icon = QIcon(icon_path)
            relation_button.setIcon(icon)
            relation_button.setIconSize(QSize(24, 24))  # 아이콘 크기 설정

            # 텍스트와 아이콘 설정
            relation_text = f"{relation_labels.get(relation, 'Unknown')}: {prob*100:.2f}%"
            relation_button.setText(relation_text)
            relation_button.setStyleSheet("text-align: left;")  # 텍스트가 아이콘 오른쪽에 위치하도록 설정

            relation_button.clicked.connect(lambda _, r=relation: self.relation_clicked.emit(r))
            self.results_layout.addWidget(relation_button)


class SingleResultPage(QWidget):
    single_clicked = pyqtSignal()

    def __init__(self):
        super().__init__()

        # 기본 레이아웃 및 위젯 생성
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # 상단 레이아웃을 위한 위젯
        self.top_layout = QVBoxLayout()
        self.top_widget = QWidget()
        self.top_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.top_widget.setLayout(self.top_layout)

        # 뒤로가기 버튼
        self.back_button = QPushButton("Back to Start Page")
        self.back_button.setObjectName("back_button")

        # 초기 상태 설정
        self.main_layout.addWidget(self.top_widget)
        self.main_layout.addWidget(self.back_button)

    def set_prediction_results(self, age_predictions, gender_predictions, detected_faces):
        self.clear_all_layouts()
        prediction_widget = QWidget()
        # 얼굴 사진 및 나이/성별 예측 결과를 중앙에 배치
        for face_id, face_img in detected_faces.items():
            gender = gender_predictions[face_id]
            age = age_predictions[face_id]
            gender_text = '남자' if gender == 0 else '여자'

            # 이미지 크기 조정
            height, width, _ = face_img.shape
            scale_factor = min(150 / width, 150 / height)
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            face_img = cv2.resize(face_img, (new_width, new_height))

            img_label = QLabel(self)
            img_label.setAlignment(Qt.AlignCenter)
            face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
            height, width, channel = face_img.shape
            bytes_per_line = 3 * width
            q_img = QImage(face_img.data, width, height, bytes_per_line, QImage.Format_RGB888)
            img_label.setPixmap(QPixmap.fromImage(q_img).scaled(150, 150, Qt.KeepAspectRatio))

            info_label = QLabel(f"나이: {age}<br>성별: {gender_text}")
            info_label.setAlignment(Qt.AlignCenter)
            info_label.setTextFormat(Qt.RichText)

            face_layout = QVBoxLayout()
            face_layout.addWidget(img_label)
            face_layout.addWidget(info_label)

            face_layout.setAlignment(Qt.AlignCenter)

        prediction_widget.setLayout(face_layout)
        self.top_layout.addWidget(prediction_widget)

        recommend_button = QPushButton("이 정보로 추천 받기")
        recommend_button.setObjectName("recommend_button")
        recommend_button.clicked.connect(self.single_clicked.emit)
        recommend_button.setFixedSize(300, 50)

        self.top_layout.addWidget(recommend_button, alignment=Qt.AlignCenter)

    def clear_all_layouts(self):
        # 상단 레이아웃 정리

        while self.top_layout.count():
            item = self.top_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

