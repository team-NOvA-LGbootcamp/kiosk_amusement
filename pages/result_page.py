from PyQt5.QtWidgets import QVBoxLayout, QHBoxLayout, QLabel, QWidget, QScrollArea, QPushButton, QSizePolicy
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtCore import Qt, pyqtSignal, QSize
import cv2

class MultiResultPage(QWidget):
    relation_clicked = pyqtSignal(str)

    def __init__(self, width, height):
        super().__init__()
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.window_width = width
        self.window_height = height

        # 상단 레이아웃 (얼굴 사진 및 나이/성별 예측 결과)
        self.top_bar = QLabel()
        self.top_bar.setFixedHeight(self.window_height*0.1)
        self.top_bar.setText('환영합니다!')
        self.top_bar.setObjectName('top_bar_label')
        self.top_bar.setAlignment(Qt.AlignCenter)
        self.top_layout = QVBoxLayout()
        self.top_widget = QWidget()
        self.top_widget.setLayout(self.top_layout)
        # self.top_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Minimum)
        self.top_widget.setObjectName('top_widget')
        self.top_widget.setFixedHeight(self.window_height*0.3)
        self.layout.addWidget(self.top_bar)
        self.layout.addWidget(self.top_widget)

        # 결과 레이아웃
        self.results_layout = QVBoxLayout()
        self.results_widget = QWidget()
        self.results_widget.setLayout(self.results_layout)
        self.results_widget.setObjectName('results_widget')
        self.results_widget.setFixedHeight(self.window_height*0.4)
        self.layout.addWidget(self.results_widget)
        

        # 뒤로가기 버튼
        self.back_button = QPushButton("처음으로 돌아가기")
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

        # 얼굴 사진 및 나이/성별 예측 결과 추가
        face_list_widget = QWidget()
        face_list_layout = QHBoxLayout()
        num_faces = len(age_predictions.keys())
        for face_id, face_img in detected_faces.items():
            gender = gender_predictions[face_id]
            age = age_predictions[face_id]
            gender_text = '남자' if gender == 0 else '여자'

            # 이미지 크기 조정: 얼굴 크기에 따라 적절한 크기로 조정
            height, width, _ = face_img.shape
            scale_factor = (self.window_width / width)  # 크기를 절반으로 줄임
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            face_img = cv2.resize(face_img, (new_width, new_height))

            img_label = QLabel(self)
            img_label.setAlignment(Qt.AlignCenter)
            face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
            height, width, channel = face_img.shape
            bytes_per_line = 3 * width
            q_img = QImage(face_img.data, width, height, bytes_per_line, QImage.Format_RGB888)
            img_label.setPixmap(QPixmap.fromImage(q_img).scaled(self.window_width*0.5/num_faces, self.window_width*0.5/num_faces, Qt.KeepAspectRatio))

            info_label = QLabel(f"나이: {age}<br>성별: {gender_text}")
            info_label.setObjectName('info_label')
            info_label.setAlignment(Qt.AlignCenter)
            info_label.setTextFormat(Qt.RichText)  # HTML 형식으로 설정

            face_layout = QVBoxLayout()
            face_layout.addWidget(img_label)
            face_layout.addWidget(info_label)

            face_list_layout.addLayout(face_layout)
        padding = QLabel()
        padding.setFixedHeight(self.window_height*0.05)
        self.top_layout.addWidget(padding)
        face_list_widget.setLayout(face_list_layout)
        self.top_layout.addWidget(face_list_widget)
        

        suggestion_label = QLabel(self)
        suggestion_label.setAlignment(Qt.AlignCenter)
        suggestion_label.setObjectName("suggestion_label")
        suggestion_label.setText("혹시 이렇게 오셨나요?")
        suggestion_label.setFixedHeight(50)
        self.results_layout.addWidget(suggestion_label)

        # 관계 예측 결과 표시
        relation_icons = {
            'friend': './resources/icons/friend.png',
            'family': './resources/icons/family.png',
            'couple': './resources/icons/couple.png'
        }
        relation_labels = {'friend' : '친구', 'family' : '가족', 'couple' : '연인'}
        sorted_relations = sorted(relation_predictions.items(), key=lambda x: x[1], reverse=True)
        for relation, prob in sorted_relations:
            relation_button = QPushButton()
            relation_button.setObjectName("relation_button")

            # 아이콘 설정
            icon_path = relation_icons.get(relation, './resources/icons/default.png')
            icon = QIcon(icon_path)
            relation_button.setIcon(icon)
            relation_button.setIconSize(QSize(36, 36))  # 아이콘 크기 설정

            # 텍스트와 아이콘 설정
            relation_text = f"{relation_labels.get(relation, 'Unknown')}: {prob*100:.2f}%"
            relation_button.setText(relation_text)
            relation_button.setStyleSheet("text-align: left;")  # 텍스트가 아이콘 오른쪽에 위치하도록 설정
            relation_button.setFixedHeight(100)

            relation_button.clicked.connect(lambda _, r=relation: self.relation_clicked.emit(r))
            self.results_layout.addWidget(relation_button)


class SingleResultPage(QWidget):
    single_clicked = pyqtSignal()

    def __init__(self, width, height):
        super().__init__()
        self.window_width = width
        self.window_height = height

        # 기본 레이아웃 및 위젯 생성
        self.main_layout = QVBoxLayout()
        self.setLayout(self.main_layout)

        # 상단 레이아웃을 위한 위젯
        self.top_bar = QLabel()
        self.top_bar.setFixedHeight(100)
        self.top_bar.setText('환영합니다!')
        self.top_bar.setObjectName('top_bar_label')
        self.top_bar.setAlignment(Qt.AlignCenter)
        self.top_layout = QVBoxLayout()
        self.top_widget = QWidget()
        self.top_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.top_widget.setObjectName('top_widget')
        self.top_widget.setLayout(self.top_layout)

        self.recommend_button = QPushButton("이 정보로 추천 받기")
        self.recommend_button.setObjectName("recommend_button")
        self.recommend_button.clicked.connect(self.single_clicked.emit)
        

        # 뒤로가기 버튼
        self.back_button = QPushButton("처음으로 돌아가기")
        self.back_button.setObjectName("back_button")

        # 초기 상태 설정
        self.main_layout.addWidget(self.top_bar)
        self.main_layout.addWidget(self.top_widget)
        self.main_layout.addWidget(self.recommend_button)
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
            scale_factor = self.window_width*0.2 / width
            new_width = int(width * scale_factor)
            new_height = int(height * scale_factor)
            face_img = cv2.resize(face_img, (new_width, new_height))

            img_label = QLabel(self)
            img_label.setAlignment(Qt.AlignCenter)
            face_img = cv2.cvtColor(face_img, cv2.COLOR_BGR2RGB)
            height, width, channel = face_img.shape
            bytes_per_line = 3 * width
            q_img = QImage(face_img.data, width, height, bytes_per_line, QImage.Format_RGB888)
            img_label.setPixmap(QPixmap.fromImage(q_img).scaled(self.window_width*0.5, self.window_width*0.5, Qt.KeepAspectRatio))

            info_label = QLabel(f"나이: {age}<br>성별: {gender_text}")
            info_label.setObjectName('single_info_label')
            info_label.setAlignment(Qt.AlignCenter)
            info_label.setTextFormat(Qt.RichText)

            face_layout = QVBoxLayout()
            face_layout.addWidget(img_label)
            face_layout.addWidget(info_label)

            face_layout.setAlignment(Qt.AlignCenter)
        
        prediction_widget.setLayout(face_layout)
        self.top_layout.addWidget(prediction_widget)

        
        under_bar = QLabel()
        under_bar.setFixedHeight(100)
        self.top_layout.addWidget(under_bar)

    def clear_all_layouts(self):
        # 상단 레이아웃 정리

        while self.top_layout.count():
            item = self.top_layout.takeAt(0)
            widget = item.widget()
            if widget:
                widget.deleteLater()

