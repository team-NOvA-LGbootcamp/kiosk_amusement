import sys
from recommendation import RecommendationAlgorithm
from PyQt5.QtWidgets import QMainWindow, QStackedWidget
from pages.camera_widget import CameraWidget
from pages.start_page import StartPage
from pages.result_page import ResultPage
from pages.amusement_park_page import AmusementParkPage


class MainWindow(QMainWindow):
    def __init__(self, model, relation_model):
        super().__init__()

        self.model = model
        self.relation_model = relation_model

        # QStackedWidget 생성
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # 첫 번째 페이지 생성 및 추가 (StartPage)
        self.start_page = StartPage()
        self.stacked_widget.addWidget(self.start_page)

        # 두 번째 페이지 생성 및 추가 (CameraWidget)
        self.camera_widget = CameraWidget()
        self.stacked_widget.addWidget(self.camera_widget)

        # 세 번째 페이지 생성 및 추가 (ResultPage)
        self.result_page = ResultPage()
        self.stacked_widget.addWidget(self.result_page)

        # 네 번째 페이지 생성 및 추가 (amusement_park_page)
        self.amusement_park_page = AmusementParkPage()
        self.stacked_widget.addWidget(self.amusement_park_page)

        # 윈도우 설정
        self.setWindowTitle("Main Window")
        self.setGeometry(100, 100, 540, 960)
        self.setFixedSize(540, 960)

        # StartPage의 start 버튼 신호와 페이지 전환 연결
        self.start_page.start_button.clicked.connect(self.show_camera_page)

        # CameraWidget의 switch_page 신호와 페이지 전환 연결
        self.camera_widget.switch_page.connect(self.show_result_page)

        self.result_page.back_button.clicked.connect(self.show_amusement_park_page)

        self.amusement_park_page.back_button.clicked.connect(self.show_start_page)
        # # ResultPage의 back 버튼 신호와 페이지 전환 연결
        # self.result_page.back_button.clicked.connect(self.show_start_page)

    def show_camera_page(self):
        self.stacked_widget.setCurrentWidget(self.camera_widget)
        self.camera_widget.start_webcam()  # 카메라 시작

    def show_result_page(self, detected_faces):
        self.camera_widget.stop_webcam()  # 웹캠 정지
        age_predictions, gender_predictions = self.model.predict_image(detected_faces)
        # relation_predictions = self.relation_model.predict_image(detected_faces, age_predictions, gender_predictions)
        relation_predictions = {
                "friend": 0.75,
                "family": 0.5,
                "couple": 0.25,
            }
        self.result_page.set_prediction_results(age_predictions, gender_predictions, detected_faces, relation_predictions)
        self.stacked_widget.setCurrentWidget(self.result_page)

    def show_start_page(self):
        self.stacked_widget.setCurrentWidget(self.start_page)

    def show_amusement_park_page(self):
        self.stacked_widget.setCurrentWidget(self.amusement_park_page)
