from PyQt5.QtCore import QTimer, pyqtSignal, Qt, QSize
from PyQt5.QtGui import QImage, QPixmap, QIcon
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
import cv2
import numpy as np
import mediapipe as mp
import math

class CameraWidget(QWidget):
    switch_page = pyqtSignal(dict)

    def __init__(self, width):
        super().__init__()
        self.window_width = width
        self.display_countdown = False
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(min_detection_confidence=0.2)
        self.cap = cv2.VideoCapture(0)
        # self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 320)
        # self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
        self.cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)
        print(f'({self.cap.get(cv2.CAP_PROP_FRAME_WIDTH),self.cap.get(cv2.CAP_PROP_FRAME_HEIGHT)})')
        
        self.appbar_label = QLabel()
        self.appbar_label.setFixedHeight(50)
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        self.countdown_label = QLabel(self)
        self.countdown_label.setAlignment(Qt.AlignCenter)
        self.countdown_label.setObjectName("countdown_label")
        self.countdown_label.setText("")
        
        self.lowbar_label = QLabel()
        self.lowbar_label.setFixedHeight(100)
        layout = QVBoxLayout()
        layout.addWidget(self.appbar_label)
        layout.addWidget(self.image_label)
        layout.addWidget(self.countdown_label)
        self.frame = None
        self.original_frame = None  # 모델에 전달할 원본 프레임

        # 카운트다운 버튼 추가
        self.capture_button = QPushButton(self)
        self.capture_button.setObjectName("capture_button")
        self.capture_button.clicked.connect(self.start_countdown)
        layout.addWidget(self.capture_button, alignment=Qt.AlignCenter)
        layout.addWidget(self.lowbar_label)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_image)
        self.timer.setInterval(30)  # 30ms마다 호출

        self.face_ids = {}
        self.angle_threshold = 20
        self.countdown_seconds = 3
        


        ## 자동촬영 구현
        self.id_checker = False
        self.id_checker_count = 0
        self.ID_CHECK_FREQUENCY = 4
        self.ID_CHECK_TIME = 250
        self.prev_face_ids = [0] * self.ID_CHECK_FREQUENCY
        self.autotimer = QTimer()
        self.autotimer.timeout.connect(self.check_face_ids)
        self.autotimer.timeout.connect(self.auto_capture)
        self.autotimer.setInterval(self.ID_CHECK_TIME)
        

        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.update_countdown)
        self.update_layout()

        container = QWidget()
        container.setLayout(layout)
        container.setObjectName("background")

        main_layout = QVBoxLayout()
        main_layout.addWidget(container)
        self.setLayout(main_layout)


    def check_face_ids(self):
        if self.face_ids:
            self.prev_face_ids[self.id_checker_count] = len(self.face_ids.keys())  
        else:
            self.prev_face_ids[self.id_checker_count] = 0
        self.id_checker_count = (self.id_checker_count + 1) % self.ID_CHECK_FREQUENCY
        if all(x == self.prev_face_ids[0] for x in self.prev_face_ids) and self.prev_face_ids[0] != 0:
            self.id_checker = True
        else:
            self.id_checker = False

    def auto_capture(self):
        if self.id_checker and not self.display_countdown:
            self.start_countdown()
        elif not self.id_checker:
            self.countdown_timer.stop()
            self.display_countdown = False
            self.capture_button.setEnabled(True)


    def update_layout(self):
        if self.display_countdown:
            # 카메라 화면 크기에 맞게 카운트다운 레이블 위치 조정
            self.countdown_label.setGeometry(
                0, 0, self.width(), 0
            )
        else:
            self.countdown_label.setGeometry(0, 0, 0, 0)

    def start_webcam(self):
        self.timer.start(30)
        self.autotimer.start(self.ID_CHECK_TIME)

    def stop_webcam(self):
        self.timer.stop()
        self.autotimer.stop()

    def start_countdown(self):
        self.countdown_seconds = 3
        self.countdown_label.setText("")
        self.display_countdown = True
        self.capture_button.setEnabled(False)
        self.update_layout()
        self.countdown_timer.start(1000)  # 1초마다 호출

    def update_countdown(self):
        self.countdown_seconds -= 1
        if self.countdown_seconds <= 0:
            self.countdown_timer.stop()
            self.countdown_label.setText("")
            if len(self.face_ids.keys()) > 0:
                self.capture_faces()
            else:
                self.countdown_label.setText("감지된 사람이 없습니다")
            self.capture_button.setEnabled(True)
            self.display_countdown = False

    def update_image(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            results = self.face_detection.process(frame)
            self.frame = frame.copy()  # 화면에 표시할 프레임
            self.original_frame = frame  # 원본 프레임
            face_boxes = []
            yaw_angles = []
            current_face_positions = {}

            if results.detections:
                for detection in results.detections:
                    yaw_angle = self.calculate_yaw_angle(detection)
                    
                    if abs(yaw_angle) <= self.angle_threshold:
                        bbox = self.get_face_bbox(frame, detection)
                        face_boxes.append(bbox)
                        yaw_angles.append(yaw_angle)
                        face_id = len(face_boxes)  # 임시로 face_id를 인덱스로 설정
                        current_face_positions[face_id] = bbox

            self.face_ids = current_face_positions

            self.draw_face_boxes(self.frame, yaw_angles)
            
            if self.display_countdown:
                self.draw_countdown_text(self.frame)
                
            self.display_frame(self.frame)

    def get_face_bbox(self, frame, detection):
        bboxC = detection.location_data.relative_bounding_box
        ih, iw, _ = frame.shape
        bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
               int(bboxC.width * iw), int(bboxC.height * ih)
        return bbox


    def capture_faces(self):
        if self.original_frame is not None:  # 원본 프레임이 존재할 경우
            face_images = {}
            for face_id, bbox in self.face_ids.items():
                x, y, w, h = bbox
                face_img = self.original_frame[y:y + h, x:x + w]  # 원본 프레임에서 얼굴 영역 잘라내기
                if face_img.size > 0:
                    face_images[face_id] = face_img  # 얼굴 ID당 하나의 이미지
            self.switch_page.emit(face_images)

    def draw_face_boxes(self, frame, yaw_angles):
        frame_height, frame_width, _ = frame.shape
    
        valid_face_ids = set()
        for face_id, bbox in list(self.face_ids.items()):  # dictionary를 리스트로 변환하여 순회
            if self.is_bbox_inside_frame(bbox, frame_width, frame_height):
                valid_face_ids.add(face_id)
                box_color = (0, 255, 0)
                cv2.rectangle(frame, bbox, box_color, 2)
    
        # 화면 밖으로 나간 얼굴 ID 삭제
        self.face_ids = {face_id: bbox for face_id, bbox in self.face_ids.items() if face_id in valid_face_ids}

    def is_bbox_inside_frame(self, bbox, frame_width, frame_height):
        x, y, w, h = bbox
        return (x >= 0 and y >= 0 and (x + w) <= frame_width and (y + h) <= frame_height)

    def draw_countdown_text(self, frame):
        countdown_text = f"{self.countdown_seconds}"
        font = cv2.FONT_HERSHEY_SIMPLEX
        font_scale = 3
        font_thickness = 10
        color = (255, 255, 255) 

        (text_width, text_height), baseline = cv2.getTextSize(countdown_text, font, font_scale, font_thickness)
        text_x = (frame.shape[1] - text_width) // 2
        text_y = (frame.shape[0] + text_height) // 2

        cv2.putText(frame, countdown_text, (text_x, text_y), font, font_scale, color, font_thickness, cv2.LINE_AA)

    def display_frame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        h, w, ch = frame.shape
        ratio = (self.window_width-30) / w
        frame = cv2.resize(frame,(int(w*ratio),int(h*ratio)))
        h, w, ch = frame.shape
        q_image = QImage(frame.data, w, h, w * ch, QImage.Format_RGB888)
        pixmap = QPixmap.fromImage(q_image)
        self.image_label.setPixmap(pixmap)

    def calculate_yaw_angle(self, detection):
        landmarks = detection.location_data.relative_keypoints
        left_eye = landmarks[self.mp_face_detection.FaceKeyPoint.LEFT_EYE]
        right_eye = landmarks[self.mp_face_detection.FaceKeyPoint.RIGHT_EYE]
        nose = landmarks[self.mp_face_detection.FaceKeyPoint.NOSE_TIP]

        eye_center_x = (left_eye.x + right_eye.x) / 2
        eye_center_y = (left_eye.y + right_eye.y) / 2

        angle_rad = math.atan2(eye_center_y - nose.y, eye_center_x - nose.x)
        angle_deg = math.degrees(angle_rad) + 90

        return angle_deg

    def closeEvent(self, event):
        if self.cap.isOpened():
            self.cap.release()
        event.accept()
