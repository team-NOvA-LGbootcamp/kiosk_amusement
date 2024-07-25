import sys
from PyQt5.QtWidgets import QMainWindow, QStackedWidget, QApplication
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtCore import QUrl
from PyQt5.QtGui import QIcon
from pages.camera_widget import CameraWidget
from pages.start_page import StartPage
from pages.result_page import MultiResultPage, SingleResultPage
from pages.amusement_park_page import AmusementParkPage
from pages.dev_camera import DevPage
import cv2
import numpy as np 
import os
import requests
import qrcode
import json
from time import time
from PIL import Image, ImageDraw, ImageFont
from datetime import datetime
import threading
import random

class MainWindow(QMainWindow):
    def __init__(self, model, relation_model, env):
        super().__init__()

        self.model = model
        self.relation_model = relation_model
        self.age_predictions = None
        self.gender_predictions = None
        self.relation_prediction = None
        self.access_token = None
        # 윈도우 설정
        self.setWindowTitle("NAMU")
        
        if env=="RASPBERRY":
            self.setGeometry(0, 0, 1080, 1920)
            self.showFullScreen()
        elif env=="DEV":
            self.setGeometry(0, 0, 540, 960)
            self.setFixedSize(540, 960)
        else:
            self.setGeometry(0, 0, 540, 960)
            self.setFixedSize(540, 960)
            # self.setGeometry(0, 0, 1080, 1920)
            # self.show_on_second_monitor()
            # self.setGeometry(0, 0, 540, 960)
            # self.setFixedSize(540, 960)


        if env=="RASPBERRY" or env=="WINDOWS":
            icon_path = './resources/icons/namu.png'
            self.icon = QIcon(icon_path)
            self.setWindowIcon(self.icon)

            # QStackedWidget 생성
            self.stacked_widget = QStackedWidget()
            self.setCentralWidget(self.stacked_widget)

            # 페이지 정의
            self.start_page = StartPage(icon_path)
            start = time()
            self.camera_widget = CameraWidget(self.width())
            end = time()
            print(f'Camera loading time : {end-start:.5f}sec')
            self.result_page_multiple = MultiResultPage(self.width(),self.height())
            self.result_page_single = SingleResultPage(self.width(),self.height())
            self.amusement_park_page = AmusementParkPage(self.width(),self.height())

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
            self.mediaPlayer.setVolume(10)
            file_path = os.path.abspath('./resources/music/puppy_waltz.mp3')
            url = QUrl.fromLocalFile(file_path)  # 음악 파일 경로 지정
            content = QMediaContent(url)
            self.mediaPlayer.setMedia(content)
            # self.mediaPlayer.play()

            # 버튼 효과음 설정
            self.button_press = QMediaPlayer()
            self.button_press.setVolume(30)
            file_path = os.path.abspath('./resources/music/button.wav')
            url = QUrl.fromLocalFile(file_path)  # 음악 파일 경로 지정
            content = QMediaContent(url)
            self.button_press.setMedia(content)

        else:
            icon_path = './resources/icons/namu.png'
            self.icon = QIcon(icon_path)
            self.setWindowIcon(self.icon)

            # QStackedWidget 생성
            self.stacked_widget = QStackedWidget()
            self.setCentralWidget(self.stacked_widget)

            # 페이지 정의
            self.start_page = StartPage(icon_path)
            self.camera_widget = DevPage()
            self.result_page_multiple = MultiResultPage(self.width(),self.height())
            self.result_page_single = SingleResultPage(self.width(),self.height())
            self.amusement_park_page = AmusementParkPage(self.width(),self.height())

            # Stacked Widget에 Attach
            self.stacked_widget.addWidget(self.start_page)
            self.stacked_widget.addWidget(self.camera_widget)
            self.stacked_widget.addWidget(self.result_page_multiple)
            self.stacked_widget.addWidget(self.result_page_single)
            self.stacked_widget.addWidget(self.amusement_park_page)


            # 버튼 액션
            self.start_page.start_button.clicked.connect(self.show_camera_page_dev)
            self.camera_widget.single_button.clicked.connect(self.show_result_dev_single)
            self.camera_widget.multi_button.clicked.connect(self.show_result_dev_multi)

            self.result_page_multiple.back_button.clicked.connect(self.show_start_page)
            self.result_page_single.back_button.clicked.connect(self.show_start_page)
            self.amusement_park_page.back_button.clicked.connect(self.show_start_page)
            self.result_page_multiple.relation_clicked.connect(self.handle_relation_clicked_dev)
            self.result_page_single.single_clicked.connect(self.handle_single_clicked_dev)

            # 배경음악 설정
            self.mediaPlayer = QMediaPlayer()
            self.mediaPlayer.setVolume(30)
            file_path = os.path.abspath('./resources/music/puppy_waltz.mp3')
            url = QUrl.fromLocalFile(file_path)  # 음악 파일 경로 지정
            content = QMediaContent(url)
            self.mediaPlayer.setMedia(content)
            # self.mediaPlayer.play()

            self.button_press = QMediaPlayer()
            self.button_press.setVolume(30)
            file_path = os.path.abspath('./resources/music/button.wav')
            url = QUrl.fromLocalFile(file_path)  # 음악 파일 경로 지정
            content = QMediaContent(url)
            self.button_press.setMedia(content)

    def show_on_second_monitor(self):
        app = QApplication.instance()
        screen = app.screens()[1] if len(app.screens()) > 1 else app.primaryScreen()
        self.setGeometry(screen.geometry())
        self.showFullScreen()

    def show_camera_page(self):
        self.button_press.play()
        self.mediaPlayer.play() # 카메라 켜지는 화면에서 재생 시작
        self.stacked_widget.setCurrentWidget(self.camera_widget)
        self.camera_widget.start_webcam()  # 카메라 시작
        self.camera_widget.prev_face_ids = [0] * self.camera_widget.ID_CHECK_FREQUENCY


    def deco_frame(self,cv2_image):
        try:
            one, two= random.sample(range(1, 10), 2)
            size = 150
            overlays = [
            {"path": f"./resources/icons/deco ({one}).png", "position": (0, 480-size), "size": (size, size)},
            {"path": f"./resources/icons/deco ({two}).png", "position": (640-size, 480-size), "size": (size, size)}
]
            # BGR을 RGB로 변환하고 PIL 이미지로 변환
            cv2_image_rgb = cv2.cvtColor(cv2_image, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(cv2_image_rgb)
            
            # 이미지 리사이즈
            pil_image = pil_image.resize((640, 480), Image.LANCZOS)

            # 오버레이 추가
            for overlay_info in overlays:
                overlay = Image.open(overlay_info["path"]).resize(overlay_info["size"], Image.LANCZOS).convert("RGBA")
                pil_image.paste(overlay, overlay_info["position"], overlay)

            # 현재 날짜와 시간 
            date_time_str = datetime.now().strftime('%Y-%m-%d %H:%M')

            # 폰트 및 색상 설정
            fonts = {
                "digital": ImageFont.truetype("./resources/fonts/digital_font.ttf", 35),
                "namu": ImageFont.truetype("./resources/fonts/Cafe24Dongdong-v2.0.ttf", 50),
                "nova": ImageFont.truetype("./resources/fonts/Cafe24Dongdong-v2.0.ttf", 15)
            }
            
            colors = {
                "digital": (255, 165, 0),
                "namu": (255, 150, 150),
                "nova": (255, 150, 150)
            }

            positions = {
                "digital": (5, 5),
                "namu": (pil_image.width - 155, 10),
                "nova": (pil_image.width - 155 - 10, 10 + 50 - 4)
            }

            # 텍스트 추가
            draw = ImageDraw.Draw(pil_image)
            draw.text(positions["digital"], date_time_str, font=fonts["digital"], fill=colors["digital"])
            draw.text(positions["namu"], "NAMU", font=fonts["namu"], fill=colors["namu"])
            draw.text(positions["nova"], "NOvA Amusement Park", font=fonts["nova"], fill=colors["nova"])

            # PIL 이미지를 다시 BGR로 변환하여 cv2 형식으로 반환
            final_image = cv2.cvtColor(np.array(pil_image), cv2.COLOR_RGB2BGR)
        except Exception as e:
            print(e)
        return final_image

        

    def generate_qr(self, iamge):
        folder = "./resources/qr/"

        if not os.path.exists(folder):
            os.makedirs(folder)

        image_path = folder+"image.jpg"
        qr_path = folder+"qr.png"
        token_path = folder+"token.json"

        try:
            if os.path.exists(qr_path):
                os.remove(qr_path)

            if not os.path.exists(token_path):
                raise Exception("no access_token file")

            with open(token_path, "r") as file:
                token_data = json.load(file)

            self.access_token = token_data.get("access_token")
            iamge = self.deco_frame(iamge)
            cv2.imwrite(image_path, iamge)

            url = "https://api.imgur.com/3/image"
            headers = {"Authorization": f"Bearer {self.access_token}",}

            with open(image_path, "rb") as image_file:
                files = {"image": image_file}
                response = requests.post(url, headers=headers, files=files)

            result = response.json()
            # print(result)
            if not result['success']:
                raise Exception("image upload fail")

            self.image_id = result["data"]["id"]
            image_link = result["data"]["link"]

            qr = qrcode.QRCode(
                version=1,
                error_correction=qrcode.constants.ERROR_CORRECT_L,
                box_size=10,
                border=4,
            )

            qr.add_data(image_link)
            qr.make(fit=True)
            img = qr.make_image(fill="black", back_color="white")
            img.save(qr_path)
        except Exception as e:
            print(e)

    def delete_img_url(self):
        try:
            if self.access_token is None:
                raise Exception("no access_token file")

            image_id = self.image_id
            url = f"https://api.imgur.com/3/image/{image_id}"
            headers = {
                "Authorization": f"Bearer {self.access_token}",
            }
            response = requests.delete(url, headers=headers)
            if response.status_code != 200:
                print("imgur delete fail")
        except Exception as e:
            print(e)

    def show_result_page(self, detected_faces):
        generate_qr_thread = threading.Thread(target=self.generate_qr,args=(self.camera_widget.frame_save,))
        generate_qr_thread.start()
        
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
        delete_img_url_thread = threading.Thread(target=self.delete_img_url)
        delete_img_url_thread.start()
        self.button_press.play()
        self.stacked_widget.setCurrentWidget(self.start_page)
        self.result_page_multiple.clear_all_layouts()
        self.result_page_single.clear_all_layouts

    def show_amusement_park_page(self):
        self.stacked_widget.setCurrentWidget(self.amusement_park_page)

    def handle_relation_clicked(self, relation):
        self.button_press.play()
        self.amusement_park_page.make_recommendation(self.age_predictions,
                                                        self.gender_predictions,
                                                        relation)
        self.stacked_widget.setCurrentWidget(self.amusement_park_page)


    def handle_single_clicked(self):
        self.button_press.play()
        self.amusement_park_page.make_recommendation(self.age_predictions,
                                                        self.gender_predictions,
                                                        "") #temporary empty string
        self.stacked_widget.setCurrentWidget(self.amusement_park_page)

    ######dev method#####
    def show_camera_page_dev(self):
        self.button_press.play()
        self.mediaPlayer.play() # 카메라 켜지는 화면에서 재생 시작
        self.stacked_widget.setCurrentWidget(self.camera_widget)

    def show_result_dev_single(self):
        self.button_press.play()
        img = cv2.imread('resources\icons\dev_image.jpg')
        detected_faces = {1:np.array(img)}
        self.age_predictions, self.gender_predictions = self.model.predict_image(detected_faces)
        self.result_page_single.set_prediction_results(self.age_predictions, self.gender_predictions, detected_faces)
        self.stacked_widget.setCurrentWidget(self.result_page_single)

    def show_result_dev_multi(self):
        self.button_press.play()
        img = cv2.imread('resources\icons\dev_image.jpg')
        img2 = cv2.imread('resources\icons\dev_image_2.png')
        detected_faces = {1:np.array(img), 2:np.array(img2)}
        self.age_predictions, self.gender_predictions = self.model.predict_image(detected_faces)
        relation_predictions = self.relation_model.predict_image(detected_faces, self.age_predictions, self.gender_predictions)
        self.result_page_multiple.set_prediction_results(self.age_predictions, self.gender_predictions, detected_faces, relation_predictions)
        self.stacked_widget.setCurrentWidget(self.result_page_multiple)

    def handle_relation_clicked_dev(self, relation):
        self.button_press.play()
        img = cv2.imread('resources\icons\dev_image.jpg')
        self.generate_qr(img)
        self.amusement_park_page.make_recommendation(self.age_predictions,
                                                        self.gender_predictions,
                                                        relation)
        self.stacked_widget.setCurrentWidget(self.amusement_park_page)


    def handle_single_clicked_dev(self):
        self.button_press.play()
        img = cv2.imread('resources\icons\dev_image.jpg')
        self.generate_qr(img)
        self.amusement_park_page.make_recommendation(self.age_predictions,
                                                        self.gender_predictions,
                                                        "") #temporary empty string
        self.stacked_widget.setCurrentWidget(self.amusement_park_page)