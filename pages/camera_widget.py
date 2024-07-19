from PyQt5.QtCore import QTimer, pyqtSignal, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
import cv2
import numpy as np
import mediapipe as mp
import math

class CameraWidget(QWidget):
    switch_page = pyqtSignal(dict)

    def __init__(self):
        super().__init__()

        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(min_detection_confidence=0.2)
        self.cap = cv2.VideoCapture(0)
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        self.frame = None

        # 카운트다운 버튼 추가
        self.countdown_button = QPushButton("Start Countdown", self)
        self.countdown_button.clicked.connect(self.start_countdown)
        layout.addWidget(self.countdown_button)

        self.setLayout(layout)
        self.setFixedSize(540, 960)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_image)
        self.timer.setInterval(30)  # 30ms마다 호출

        self.face_ids = {}
        self.angle_threshold = 20
        self.countdown_seconds = 3

        self.countdown_timer = QTimer()
        self.countdown_timer.timeout.connect(self.update_countdown)

    def start_webcam(self):
        self.timer.start(30)

    def stop_webcam(self):
        self.timer.stop()

    def start_countdown(self):
        self.countdown_seconds = 3
        self.countdown_button.setEnabled(False)
        self.countdown_button.setText(f"Starting in {self.countdown_seconds}...")
        self.countdown_timer.start(1000)  # 1초마다 호출

    def update_countdown(self):
        self.countdown_seconds -= 1
        if self.countdown_seconds <= 0:
            self.countdown_timer.stop()
            self.countdown_button.setText("Capturing...")
            self.capture_faces()
            self.countdown_button.setEnabled(True)
            self.countdown_button.setText("Start Countdown")
        else:
            self.countdown_button.setText(f"Starting in {self.countdown_seconds}...")

    def update_image(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            results = self.face_detection.process(frame)
            self.frame = frame
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
                        self.draw_face_annotations(frame, bbox, yaw_angle)

            self.face_ids = current_face_positions

            self.draw_face_boxes(frame, yaw_angles)
            self.display_frame(frame)

    def get_face_bbox(self, frame, detection):
        bboxC = detection.location_data.relative_bounding_box
        ih, iw, _ = frame.shape
        bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
               int(bboxC.width * iw), int(bboxC.height * ih)
        return bbox

    def draw_face_annotations(self, frame, bbox, yaw_angle):
        cv2.putText(frame, f'Angle: {yaw_angle:.2f}', (bbox[0], bbox[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

    def capture_faces(self):
        if self.frame is not None:  # 현재 프레임이 존재할 경우
            face_images = {}
            for face_id, bbox in self.face_ids.items():
                x, y, w, h = bbox
                face_img = self.frame[y:y + h, x:x + w]
                if face_img.size > 0:
                    face_images[face_id] = face_img  # 얼굴 ID당 하나의 이미지
            self.switch_page.emit(face_images)

    def draw_face_boxes(self, frame, yaw_angles):
        frame_height, frame_width, _ = frame.shape
    
        valid_face_ids = set()
        for face_id, bbox in list(self.face_ids.items()):  # dictionary를 리스트로 변환하여 순회
            if self.is_bbox_inside_frame(bbox, frame_width, frame_height):
                valid_face_ids.add(face_id)
                yaw_angle = yaw_angles[face_id] if face_id < len(yaw_angles) else 0
                box_color = (0, 255, 0) if abs(yaw_angle) <= self.angle_threshold else (255, 0, 0)
                cv2.rectangle(frame, bbox, box_color, 2)
                cv2.putText(frame, f'ID: {face_id}', (bbox[0], bbox[1] - 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, box_color, 2)
    
        # 화면 밖으로 나간 얼굴 ID 삭제
        self.face_ids = {face_id: bbox for face_id, bbox in self.face_ids.items() if face_id in valid_face_ids}

    def is_bbox_inside_frame(self, bbox, frame_width, frame_height):
        x, y, w, h = bbox
        return (x >= 0 and y >= 0 and (x + w) <= frame_width and (y + h) <= frame_height)

    def display_frame(self, frame):
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
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
