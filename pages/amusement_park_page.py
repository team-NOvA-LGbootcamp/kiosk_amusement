from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPixmap, QColor, QMovie
from PyQt5.QtCore import Qt, QByteArray, pyqtSignal, QSize
from recommendation import RecommendationAlgorithm
import os
import random


rides_name = {
    "bumper_cars": "범퍼카",
    "ferris_wheel": "대관람차",
    "haunted_house": "귀신의 집",
    "merry_go_round": "회전목마",
    "roller_coaster": "롤러코스터",
    "safari": "사파리",
    "swing_ride": "회전그네",
    "themepark_train": "호수 열차",
    "viking": "바이킹"
}

class AmusementParkPage(QWidget):
    recommendation_complete = pyqtSignal()

    def __init__(self, width, height):
        super().__init__()
        self.window_width = width
        self.window_height = height
        self.recbox_width = self.window_width*0.3
        self.recbox_height = self.window_height*0.1
        self.rides_loc = {
            "bumper_cars": (self.window_width*0.6, self.window_height/4), 
            "ferris_wheel": (self.window_width*0.13, self.window_height/3.8),
            "haunted_house": (self.window_width*0.63, self.window_height/5.2),
            "merry_go_round": (self.window_width*0.45, self.window_height/5.5),
            "roller_coaster": (self.window_width*0.38, self.window_height/12),
            "safari": (self.window_width*0.28, self.window_height/7.2),
            "swing_ride": (self.window_width*0.75, self.window_height/3.4),
            "themepark_train": (self.window_width*0.4, self.window_height/4), 
            "viking": (self.window_width*0.8, self.window_height/5.4),
        }
        self.recommendation_res= []

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(Qt.white))
        self.setPalette(palette)

        # Intro Text 영역
        intro_widget = QWidget()
        intro_widget.setFixedHeight(self.window_height/9)
        intro_layout = QVBoxLayout()
        intro_widget.setLayout(intro_layout)
        intro_text_label = QLabel("NOvA Park에 오신 것을 환영합니다.\n아래 어트랙션을 추천드려요!", self)
        intro_text_label.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        intro_text_label.setObjectName('attraction_guide_label')
        intro_layout.addWidget(intro_text_label)

        # Recommendation 영역       
        recommendation_widget = QWidget()
        recommendation_widget.setFixedHeight(self.window_height/7)
        recommendation_widget.setObjectName("outer_recommendation_widget")  # objectName 지정
        recommendation_layout = QHBoxLayout()
        recommendation_widget.setLayout(recommendation_layout)
        
        loading_label = QLabel()
        loading_label.setFixedSize(self.window_width*0.15, self.window_width*0.15)
        loading_label.setAlignment(Qt.AlignCenter)
        movie = QMovie('./resources/icons/loading.gif', QByteArray(), self)
        movie.setCacheMode(QMovie.CacheAll)
        loading_label.setMovie(movie)
        movie.setScaledSize(QSize(self.window_width*0.15, self.window_width*0.15))
        movie.start()
        recommendation_layout.addWidget(loading_label)

        # Park Map 영역
        self.parkmap_widget = QWidget()
        parkmap_layout = QVBoxLayout()
        self.parkmap_widget.setLayout(parkmap_layout)
        parkmap_label = QLabel()
        parkmap_label.setPixmap(QPixmap("./resources/icons/park.png").scaled(self.window_width*0.85, self.window_width*0.85))
        parkmap_label.setScaledContents(True)
        parkmap_label.setAlignment(Qt.AlignCenter)
        parkmap_layout.addWidget(parkmap_label)
        
        # Park Map에 Current Loc 아이콘 추가
        icon1_label = QLabel(self.parkmap_widget)
        icon1_label.setFixedSize((self.window_width*0.06), (self.window_width*0.06))
        movie = QMovie('./resources/icons/current_location.gif', QByteArray(), self)
        movie.setCacheMode(QMovie.CacheAll)
        movie.setScaledSize(QSize(self.window_width*0.06,self.window_width*0.06))
        icon1_label.setMovie(movie)
        icon1_label.move(self.window_width*0.585, self.window_width*0.67) # 이미지 위치 설정
        movie.start()

        # Park Map에 ghost 이미지 추가
        icon2_label = QLabel(self.parkmap_widget)
        icon2_label.setFixedSize((self.window_width*0.07), (self.window_width*0.07))
        icon2_label.setPixmap(QPixmap("./resources/icons/ghost.png").scaled(self.window_width*0.07, self.window_width*0.07))
        icon2_label.move((self.window_width*0.65), (self.window_height*0.18)) # 이미지 위치 설정
        
        # QR코드 영역
        self.photozone_widget = QWidget()
        self.photozone_layout = QHBoxLayout()
        self.photozone_widget.setLayout(self.photozone_layout)
        
        # 각 영역을 메인 레이아웃에 추가
        main_layout.addWidget(intro_widget)
        main_layout.addWidget(recommendation_widget)
        main_layout.addWidget(self.parkmap_widget)
        main_layout.addWidget(self.photozone_widget)
        main_layout.setSpacing(0)

        # Back 버튼
        self.back_button = QPushButton("처음으로 돌아가기")
        self.back_button.setObjectName("back_button")
        main_layout.addWidget(self.back_button)
    
    def make_recommendation(self, ages, genders, relation):
        recommendation = RecommendationAlgorithm()
        self.recommendation_res = recommendation.run_recommendation(ages, genders, relation)
        self.update_recommendations()  # 추천 결과 업데이트
        self.update_qrcode_image()  # QR 코드 및 이미지 업데이트
        

    def update_recommendations(self):
        recommendation_layout = self.layout().itemAt(1).widget().layout()
        
        # 기존 위젯들 제거
        for i in reversed(range(recommendation_layout.count())):
            item = recommendation_layout.itemAt(i)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)

        for widget in self.parkmap_widget.findChildren(QLabel):
            if widget.objectName() == "target_loc_label":
                widget.setParent(None)

        for i, res in enumerate(self.recommendation_res):
            box = QWidget()
            box_layout = QVBoxLayout()
            box.setLayout(box_layout)

            num = random.randrange(2, 9)
            title_label = QLabel(f"{i+1}. {rides_name[res]}\n대기시간: {num*15}분")
            title_label.setObjectName('attraction_time_label')
            title_label.setFixedHeight(self.window_height//18)
            title_label.setAlignment(Qt.AlignTop | Qt.AlignCenter)
            box_layout.addWidget(title_label)

            image_label = QLabel()
            pixmap = QPixmap(f"./resources/icons/{res}.png")  # 각 박스에 맞는 이미지 파일 경로 설정
            image_label.setPixmap(pixmap.scaled(self.window_width*0.1,self.window_width*0.1))
            image_label.setAlignment(Qt.AlignCenter | Qt.AlignTop)
            box_layout.addWidget(image_label)

            box_layout.setContentsMargins(0,0,0,0)
            recommendation_layout.addWidget(box)
            recommendation_layout.setContentsMargins(0,0,0,0)

            target_loc_label = QLabel(self.parkmap_widget)
            target_loc_label.setObjectName("target_loc_label")
            target_loc_label.setFixedSize((self.window_width*0.1), (self.window_width*0.1))
            movie = QMovie('./resources/icons/target_loc.gif', QByteArray(), self)
            movie.setCacheMode(QMovie.CacheAll)
            movie.setScaledSize(QSize(self.window_width*0.1,self.window_width*0.1))
            target_loc_label.setMovie(movie)
            target_loc_label.move(self.rides_loc[res][0], self.rides_loc[res][1]) # 이미지 위치 설정
            movie.start()

        self.recommendation_complete.emit()
    
    def update_qrcode_image(self):
        for i in reversed(range(self.photozone_layout.count())):
            item = self.photozone_layout.itemAt(i)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)

        photo_path = "./resources/qr/image.jpg"
        qr_path = "./resources/qr/qr.png"
        photo_size_w, photo_size_h = self.window_width*0.5, self.window_width*0.35
        qr_size_w, qr_size_h = self.window_width*0.15, self.window_width*0.15

        self.photo_label = QLabel()
        self.photo_label.setFixedSize(photo_size_w, photo_size_h)
        self.qrcode_label = QLabel()
        self.qrcode_label.setFixedSize(qr_size_w, qr_size_h)

        if os.path.exists(photo_path):
            pixmap = QPixmap(photo_path)
            self.photo_label.setPixmap(pixmap.scaled(photo_size_w, photo_size_h))
            self.photozone_layout.addWidget(self.photo_label)
        if os.path.exists(qr_path):
            pixmap_2 = QPixmap(qr_path)
            self.qrcode_label.setPixmap(pixmap_2.scaled(qr_size_w, qr_size_h))
            self.photozone_layout.addWidget(self.qrcode_label)