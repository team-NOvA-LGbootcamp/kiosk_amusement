from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QGridLayout
from PyQt5.QtGui import QPainter, QColor, QBrush, QPixmap, QPen, QFont
from PyQt5.QtCore import Qt, QRectF


class AmusementParkPage(QWidget):
    def __init__(self, recommendation_res=[]):
        super().__init__()

        self.layout = QVBoxLayout()
        self.results_layout = QGridLayout()
        self.layout.addLayout(self.results_layout)

        self.back_button = QPushButton("Back to Start Page")
        self.back_button.clicked.connect(self.back_to_start_page)
        self.layout.addWidget(self.back_button)

        self.text_space=300

        # Display background image using QLabel
        self.background_image = QPixmap('../ui_images/park.png') # 배경 이미지 로드
        self.background_label = QLabel(self)
        self.background_label.setPixmap(self.background_image)
        self.results_layout.addWidget(self.background_label, 0, 0, 1, 1)
        # self.background_label.setGeometry(0, self.text_space, self.background_image.width(), self.background_image.height())
        # self.background_label.setScaledContents(True)  # Scale pixmap to fit QLabel
        
        # Add background_label to layout
        self.results_layout.addWidget(self.background_label)
        
        self.recommendation_res = recommendation_res

        # 현위치
        self.kiosk = (self.background_image.width()*5/8-10, self.background_image.height()*4/5-10)
        # 놀이기구 좌표(x,y)
        self.ferris_wheel = (self.background_image.width()*1.5/9, self.background_image.height()*4/6)
        self.bumper_cars = (self.background_image.width()*6/9, self.background_image.height()*2/3)
        self.merry_go_round = (self.background_image.width()*1/2, self.background_image.height()*2.3/5)
        self.roller_coaster = (self.background_image.width()*3/5, self.background_image.height()*1/4)
        self.viking = (self.background_image.width()*4/5, self.background_image.height()*1/2)
        self.swing_ride = (self.background_image.width()*3/4, self.background_image.height()*3/5)
        self.safari = (self.background_image.width()*5.5/9, self.background_image.height()*1/2-10) # horror house?
        self.themepark_train = (self.background_image.width()*1.5/9, self.background_image.height()*4/6)

        self.setLayout(self.layout)
        

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        # 기본 배경 skeleton 설정
        # painter.drawPixmap(0, self.text_space, 700, 700, self.background_image)
        painter.fillRect(0, 0, self.background_image.width(), self.text_space, QColor(255, 255, 255))
        
        # 펜 설정
        painter.setPen(QColor(0, 0, 0))
        painter.setFont(QFont("Arial", 15))

        # 인삿말 표시
        text_rect = QRectF(0,0, self.background_image.width(), 50)  # x, y, width, height
        painter.drawText(text_rect, Qt.AlignCenter | Qt.AlignTop, "환영합니다!")

        # Kiosk 표시
        self.draw_curr_loc(painter, self.kiosk, 20)
        # 놀이기구 표시
        self.draw_rides(painter, self.ferris_wheel, 20)
        self.draw_rides(painter, self.bumper_cars, 20)
        self.draw_rides(painter, self.merry_go_round, 20)
        self.draw_rides(painter, self.roller_coaster, 20)
        self.draw_rides(painter, self.viking, 20)
        self.draw_rides(painter, self.swing_ride, 20)
        self.draw_rides(painter, self.safari, 20)
        self.draw_rides(painter, self.themepark_train, 20)

        # 추천 결과 표시
        painter.setFont(QFont("Arial", 12))
        # res_text = self.recommendation_res
        res_text = ["Viking", "Safari", "ferris wheel"]
        for i, res in enumerate(res_text):
            painter.drawText(QRectF(self.background_image.width()/3*i,50, self.background_image.width()/3, 50),
                             Qt.AlignCenter,
                             f"{i+1}: {res}")
            painter.drawPixmap(self.background_image.width()/3*i+70,100, 70, 70, QPixmap(f"../ui_images/{res.lower()}.png"))


    def draw_curr_loc(self, painter, loc, size):
        painter.setBrush(QColor(0, 0, 255))
        painter.drawEllipse(loc[0], loc[1], size, size)
   
    def draw_rides(self, painter, ride, size):
        painter.setBrush(QColor(255,255,0))
        painter.drawEllipse(ride[0], ride[1]+self.text_space, size, size)
    
    def back_to_start_page(self):
        self.parentWidget().setCurrentIndex(0)  # Switch to start page
