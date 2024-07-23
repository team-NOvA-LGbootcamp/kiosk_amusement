import sys
from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QApplication
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
from pages.camera_widget import CameraWidget
from pages.start_page import StartPage
from pages.result_page import MultiResultPage, SingleResultPage
from pages.amusement_park_page import AmusementParkPage


class MainWindow(QMainWindow):
    def __init__(self, model, relation_model):
        super().__init__()

        self.model = model
        self.relation_model = relation_model
        self.age_predictions = None
        self.gender_predictions = None
        self.relation_prediction = None

        # 윈도우 설정
        self.setWindowTitle("NAMU")
        self.setGeometry(0, 0, 540, 960)
        self.setFixedSize(540, 960)
        # self.show_on_second_monitor()
        icon_path = './resources/icons/namu.png'
        self.icon = QIcon(icon_path)
        self.setWindowIcon(self.icon)

        # QStackedWidget 생성
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)

        # 페이지 정의
        self.start_page = StartPage(icon_path)
        self.camera_widget = CameraWidget()
        self.result_page_multiple = MultiResultPage()
        self.result_page_single = SingleResultPage()
        self.amusement_park_page = AmusementParkPage()

        # Stacked Widget에 Attach
        self.stacked_widget.addWidget(self.start_page)
        self.stacked_widget.addWidget(self.camera_widget)
        self.stacked_widget.addWidget(self.result_page_multiple)
        self.stacked_widget.addWidget(self.result_page_single)
        self.stacked_widget.addWidget(self.amusement_park_page)


        # 버튼 액션
        self.start_page.start_button.clicked.connect(self.show_camera_page)
        self.camera_widget.switch_page.connect(self.show_result_page)
        self.result_page_multiple.back_button.clicked.connect(self.show_start_page)
        self.result_page_single.back_button.clicked.connect(self.show_start_page)
        self.amusement_park_page.back_button.clicked.connect(self.show_start_page)
        self.result_page_multiple.relation_clicked.connect(self.handle_relation_clicked)
        self.result_page_single.single_clicked.connect(self.handle_single_clicked)

        # 배경음악 설정
        self.mediaPlayer = QMediaPlayer()
        self.mediaPlayer.setVolume(30)
        url = QUrl.fromLocalFile('./resources/music/puppy_waltz.mp3')  # 음악 파일 경로 지정
        content = QMediaContent(url)
        self.mediaPlayer.setMedia(content)
        # self.mediaPlayer.play()


    def show_on_second_monitor(self):
        app = QApplication.instance()
        screen = app.screens()[1] if len(app.screens()) > 1 else app.primaryScreen()
        self.setGeometry(screen.geometry())
        self.showFullScreen()

    def show_camera_page(self):
        self.mediaPlayer.play() # 카메라 켜지는 화면에서 재생 시작

        self.stacked_widget.setCurrentWidget(self.camera_widget)
        self.camera_widget.start_webcam()  # 카메라 시작

    def show_result_page(self, detected_faces):
        self.camera_widget.stop_webcam()  # 웹캠 정지
        self.age_predictions, self.gender_predictions = self.model.predict_image(detected_faces)
        if len(self.age_predictions.keys()) > 1:
            relation_predictions = self.relation_model.predict_image(detected_faces, self.age_predictions, self.gender_predictions)
            self.result_page_multiple.set_prediction_results(self.age_predictions, self.gender_predictions, detected_faces, relation_predictions)
            self.stacked_widget.setCurrentWidget(self.result_page_multiple)
        else:
            self.result_page_single.set_prediction_results(self.age_predictions, self.gender_predictions, detected_faces)
            self.stacked_widget.setCurrentWidget(self.result_page_single)

    def show_start_page(self):
        self.stacked_widget.setCurrentWidget(self.start_page)
        self.result_page_multiple.clear_all_layouts()
        self.result_page_single.clear_all_layouts

    def show_amusement_park_page(self):
        self.stacked_widget.setCurrentWidget(self.amusement_park_page)

    def handle_relation_clicked(self, relation):
        self.amusement_park_page.make_recommendation(self.age_predictions,
                                                        self.gender_predictions,
                                                        relation)
        self.stacked_widget.setCurrentWidget(self.amusement_park_page)


    def handle_single_clicked(self):
        self.amusement_park_page.make_recommendation(self.age_predictions,
                                                        self.gender_predictions,
                                                        "") #temporary empty string
        self.stacked_widget.setCurrentWidget(self.amusement_park_page)