from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QFrame, QSpacerItem, QSizePolicy
from PyQt5.QtGui import QPixmap, QColor, QMovie
from PyQt5.QtCore import Qt, QByteArray, pyqtSignal, QSize
from recommendation import RecommendationAlgorithm
import os

class AmusementParkPage(QWidget):
    recommendation_complete = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.recommendation_res= []
        self.recbox_width = self.width()*0.28
        self.recbox_height = self.height()*0.36

        main_layout = QVBoxLayout(self)
        main_layout.setSpacing(0)
        self.setLayout(main_layout)

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(self.backgroundRole(), QColor(Qt.white))
        self.setPalette(palette)

        # Intro Text 영역
        intro_widget = QWidget()
        intro_layout = QVBoxLayout()
        intro_widget.setLayout(intro_layout)
        intro_text_label = QLabel("NOvA Park에 오신 것을 환영합니다.\n아래 어트랙션을 추천드려요!", self)
        intro_text_label.setAlignment(Qt.AlignTop | Qt.AlignCenter)
        intro_text_label.setObjectName('attraction_guide_label')
        intro_layout.addWidget(intro_text_label)

        # Recommendation 영역       
        recommendation_widget = QWidget()
        recommendation_widget.setObjectName("outer_recommendation_widget")  # objectName 지정
        recommendation_layout = QHBoxLayout()
        recommendation_widget.setLayout(recommendation_layout)
        
        loading_label = QLabel()
        loading_label.setFixedSize(int(self.width()*0.15), int(self.width()*0.15))
        loading_label.setAlignment(Qt.AlignCenter)
        movie = QMovie('./resources/icons/loading.gif', QByteArray(), self)
        movie.setCacheMode(QMovie.CacheAll)
        loading_label.setMovie(movie)
        movie.setScaledSize(QSize(int(self.width()*0.15), int(self.width()*0.15)))
        movie.start()
        recommendation_layout.addWidget(loading_label)

        # parkmap 영역
        parkmap_widget = QWidget()
        parkmap_layout = QVBoxLayout()
        parkmap_widget.setLayout(parkmap_layout)

        parkmap_label = QLabel()
        parkmap_label.setPixmap(QPixmap("./resources/icons/park.png").scaledToWidth(self.width()))
        parkmap_label.setScaledContents(True)
        parkmap_label.setAlignment(Qt.AlignTop)
        parkmap_layout.addWidget(parkmap_label)
        
        # Park Map에 Current Loc 아이콘 추가
        icon1_label = QLabel(parkmap_widget)
        icon1_label.setFixedSize(int(self.width()*0.07), int(self.width()*0.07))
        movie = QMovie('./resources/icons/current_location.gif', QByteArray(), self)
        movie.setCacheMode(QMovie.CacheAll)
        movie.setScaledSize(QSize(int(self.width()*0.07), int(self.width()*0.07)))
        icon1_label.setMovie(movie)
        icon1_label.move(int(self.width()*0.47), int(self.height()*0.65)) # 이미지 위치 설정
        movie.start()

        # Park Map에 ghost 이미지 추가
        icon2_label = QLabel(parkmap_widget)
        icon2_label.setFixedSize(int(self.width()*0.08), int(self.width()*0.08))
        icon2_label.setPixmap(QPixmap("./resources/icons/ghost.png").scaled(int(self.width()*0.08), int(self.width()*0.08)))
        icon2_label.move(int(self.width()*0.52), int(self.height()*0.3)) # 이미지 위치 설정

        # QR코드 공간 추가 (Label을 이용)
        qrcode_label = QLabel()
        qrcode_label.setFixedSize(self.width(), self.width()//4)
        if os.path.exists("./resources/qr/image.jpg"):
            # 이미지 추가 예시 (두 개의 이미지를 추가)
            qrcode_layout = QHBoxLayout(qrcode_label)

            image1_label = QLabel()
            image1_label.setPixmap(QPixmap("./resources/qr/image.jpg").scaledToWidth(self.width()//4))
            image1_label.setAlignment(Qt.AlignCenter)
            qrcode_layout.addWidget(image1_label)
            if os.path.exists("./resources/qr/qr.png"):
                image2_label = QLabel()
                image2_label.setPixmap(QPixmap("./resources/qr/qr.png").scaledToWidth(60))
                image2_label.setAlignment(Qt.AlignCenter|Qt.AlignLeft)
                qrcode_layout.addWidget(image2_label)
        
        # 각 영역을 메인 레이아웃에 추가
        main_layout.addWidget(intro_widget)
        main_layout.addWidget(recommendation_widget)
        main_layout.addWidget(parkmap_widget)
        main_layout.addWidget(qrcode_label)
        main_layout.setSpacing(0)

        # Back 버튼
        self.back_button = QPushButton("Back to Start Page")
        self.back_button.setObjectName("back_button")
        main_layout.addWidget(self.back_button)
    
    def make_recommendation(self, ages, genders, relation):
        recommendation = RecommendationAlgorithm()
        self.recommendation_res = recommendation.run_recommendation(ages, genders, relation)
        self.update_recommendations()  # 추천 결과 업데이트

    def update_recommendations(self):
        recommendation_layout = self.layout().itemAt(1).widget().layout()
        
        # 기존 위젯들 제거
        for i in reversed(range(recommendation_layout.count())):
            item = recommendation_layout.itemAt(i)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)

        for i, res in enumerate(self.recommendation_res):
            box = QWidget()
            box.setFixedSize(int(self.recbox_width), int(self.recbox_height))
            box_layout = QVBoxLayout()
            box.setLayout(box_layout)
            box_layout.setContentsMargins(0,0,0,0)

            ride_name = " ".join([word.title() for word in res.split("_")])
            title_label = QLabel(f"{i+1}: {ride_name}\n대기시간: {35*(i+1)}분")
            title_label.setObjectName('attraction_time_label')
            title_label.setAlignment(Qt.AlignTop | Qt.AlignCenter)
            box_layout.addWidget(title_label)

            image_label = QLabel()
            pixmap = QPixmap(f"./resources/icons/{res}.png")  # 각 박스에 맞는 이미지 파일 경로 설정
            image_label.setPixmap(pixmap.scaled(int(self.width()*0.11), int(self.width()*0.11)))
            image_label.setAlignment(Qt.AlignCenter | Qt.AlignTop)
            box_layout.addWidget(image_label)

            recommendation_layout.addWidget(box)

        self.recommendation_complete.emit()