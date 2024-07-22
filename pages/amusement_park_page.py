from PyQt5.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QPushButton, QApplication
from PyQt5.QtGui import QPixmap, QColor, QMovie
from PyQt5.QtCore import Qt, QByteArray, pyqtSignal
from recommendation import RecommendationAlgorithm


class AmusementParkPage(QWidget):
    recommendation_complete = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.recommendation_res= []
        # self.recommendation_res = recommendation_res or ["viking", "ferris_wheel", "safari"]

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
        intro_text_label.setAlignment(Qt.AlignCenter)
        intro_text_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        intro_layout.addWidget(intro_text_label)

        # Recommendation 영역
        recommendation_widget = QWidget()
        recommendation_layout = QHBoxLayout()
        recommendation_widget.setLayout(recommendation_layout)

        self.recbox_width = self.width() // 3
        self.recbox_height = 250
        for i in range(3):
            box = QWidget()
            box.setFixedSize(self.recbox_width, self.recbox_height)
            box_layout = QVBoxLayout()
            box.setLayout(box_layout)

            image_label = QLabel()
            # 동적 이미지 추가 (loading.gif)
            movie = QMovie('./ui_images/loading.gif', QByteArray(), self)
            movie.setCacheMode(QMovie.CacheAll)
            image_label.setMovie(movie)
            movie.start()

            # image_label.setPixmap(pixmap.scaled(70,70))
            image_label.setAlignment(Qt.AlignCenter)
            box_layout.addWidget(image_label)

            recommendation_layout.addWidget(box)

        # parkmap 영역
        parkmap_widget = QWidget()
        parkmap_layout = QVBoxLayout()
        parkmap_widget.setLayout(parkmap_layout)

        parkmap_label = QLabel()
        parkmap_label.setPixmap(QPixmap("./ui_images/park.png"))
        parkmap_label.setAlignment(Qt.AlignCenter)
        parkmap_label.setScaledContents(True)
        parkmap_layout.addWidget(parkmap_label)
        
        # Current Location 아이콘 추가
        icon_label = QLabel(parkmap_widget)
        location_icon = QPixmap("./ui_images/current_loc.png")
        icon_label.setPixmap(location_icon.scaled(32,35))
        icon_label.move(273, 440) # 이미지 위치 설정
        icon_label.setAlignment(Qt.AlignCenter)

        # 각 영역을 메인 레이아웃에 추가
        main_layout.addWidget(intro_widget)
        main_layout.addWidget(recommendation_widget)
        main_layout.addWidget(parkmap_widget)

        # Back 버튼
        self.back_button = QPushButton("Back to Start Page")
        main_layout.addWidget(self.back_button, alignment=Qt.AlignBottom | Qt.AlignCenter)
    
    def make_recommendation(self, ages, genders, relation):
        recommendation = RecommendationAlgorithm()
        self.recommendation_res = recommendation.run_recommendation(ages, genders, relation)
        self.update_recommendations()  # 추천 결과 업데이트

    def update_recommendations(self):
        recommendation_layout = self.layout().itemAt(1).widget().layout()  # Recommendation 영역의 layout 가져오기
        
        # 기존 위젯들 제거
        for i in reversed(range(recommendation_layout.count())):
            widget = recommendation_layout.itemAt(i).widget()
            widget.setParent(None)

        for i, res in enumerate(self.recommendation_res):
            box = QWidget()
            box.setFixedSize(self.recbox_width, self.recbox_height)
            box_layout = QVBoxLayout()
            box.setLayout(box_layout)

            ride_name = " ".join([word.title() for word in res.split("_")])
            title_label = QLabel(f"{i+1}: {ride_name}")
            title_label.setStyleSheet("font-size: 16px;")
            title_label.setAlignment(Qt.AlignCenter)
            box_layout.addWidget(title_label)

            image_label = QLabel()
            pixmap = QPixmap(f"./ui_images/{res}.png")  # 각 박스에 맞는 이미지 파일 경로 설정
            image_label.setPixmap(pixmap.scaled(70,70))
            image_label.setAlignment(Qt.AlignCenter)
            box_layout.addWidget(image_label)

            recommendation_layout.addWidget(box)

        self.recommendation_complete.emit()