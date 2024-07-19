import cv2
import numpy as np
import mediapipe as mp
from PyQt5.QtCore import QTimer, pyqtSignal, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
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
        layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        self.setFixedSize(540, 960)

        self.timer = QTimer()
        self.timer.timeout.connect(self.update_image)
        self.timer.setInterval(30)  # 30ms마다 호출

        self.last_face_positions = {}
        self.angle_within_range_start_time = None
        self.angle_threshold = 15
        self.position_threshold = 100
        self.required_duration = 3000  # milliseconds
        self.face_images_buffer = {}
        self.face_ids = {}
        self.image_capture_interval = 250  # 250ms마다 이미지를 저장 (초당 4개)
        self.last_capture_time = 0
        self.condition_not_met = False  # 조건 미충족 플래그

        self.message_label = QLabel(self)
        self.message_label.setAlignment(Qt.AlignCenter)
        self.message_label.setStyleSheet("QLabel { color : red; }")
        layout.addWidget(self.message_label)

    def update_image(self):
        ret, frame = self.cap.read()
        if ret:
            frame = cv2.flip(frame, 1)
            results = self.face_detection.process(frame)

            face_detected = False
            current_face_positions = {}
            face_boxes = []
            yaw_angles = []  # 얼굴의 yaw 각도를 저장할 리스트

            if results.detections:
                face_detected = True
                for detection in results.detections:
                    bbox = self.get_face_bbox(frame, detection)
                    face_boxes.append(bbox)

                    yaw_angle = self.calculate_yaw_angle(detection)
                    yaw_angles.append(yaw_angle)  # 저장
                    self.draw_face_annotations(frame, bbox, yaw_angle)

                current_face_positions = {i: bbox for i, bbox in enumerate(face_boxes)}
                self.update_face_ids(current_face_positions)

                all_faces_satisfy_condition = self.check_all_faces_conditions(results.detections)
                self.handle_face_capture(frame, all_faces_satisfy_condition)

            else:
                self.reset_tracking()

            self.draw_face_boxes(frame, yaw_angles)  # 각도 정보를 함께 전달
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

    def update_face_ids(self, current_face_positions):
        matched_face_ids = set()
        updated_face_ids = {}
        new_face_id = 1 if not self.face_ids else max(self.face_ids.keys()) + 1

        for i, bbox in current_face_positions.items():
            matched = False
            for face_id, last_bbox in self.face_ids.items():
                if np.linalg.norm(np.array(bbox[:2]) - np.array(last_bbox[:2])) < self.position_threshold:
                    matched_face_ids.add(face_id)
                    updated_face_ids[face_id] = bbox
                    matched = True
                    break
            if not matched:
                updated_face_ids[new_face_id] = bbox
                matched_face_ids.add(new_face_id)
                new_face_id += 1

        if set(self.face_ids.keys()) != matched_face_ids:
            self.reset_tracking()

        self.face_ids = updated_face_ids

    def check_all_faces_conditions(self, detections):
        return all(abs(self.calculate_yaw_angle(detection)) <= self.angle_threshold for detection in detections)

    def handle_face_capture(self, frame, all_faces_satisfy_condition):
        current_time = cv2.getTickCount() / cv2.getTickFrequency() * 1000

        if all_faces_satisfy_condition:
            self.condition_not_met = False
            if self.angle_within_range_start_time is None:
                self.angle_within_range_start_time = current_time
            
            if current_time - self.last_capture_time >= self.image_capture_interval:
                self.last_capture_time = current_time
                self.capture_faces(frame)

            elapsed_time = current_time - self.angle_within_range_start_time
            if elapsed_time >= self.required_duration:
                self.switch_page.emit(self.face_images_buffer)
                self.reset_tracking()
        else:
            self.reset_tracking()

    def capture_faces(self, frame):
        for face_id in self.face_ids.keys():
            bbox = self.face_ids[face_id]
            face_img = frame[bbox[1]:bbox[1] + bbox[3], bbox[0]:bbox[0] + bbox[2]]
            if face_img.size > 0:
                if face_id not in self.face_images_buffer:
                    self.face_images_buffer[face_id] = []
                self.face_images_buffer[face_id].append(face_img)

    def reset_tracking(self):
        self.angle_within_range_start_time = None
        self.condition_not_met = True
        self.face_images_buffer = {}

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
            else:
                # 화면 밖으로 나간 얼굴 ID는 나중에 삭제
                valid_face_ids.add(face_id)
    
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

        if self.condition_not_met:
            self.message_label.setText("조건 미충족: 타이머 초기화")
        else:
            self.message_label.clear()

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

    def stop_webcam(self):
        self.timer.stop()

    def start_webcam(self):
        self.timer.start(30)

    def closeEvent(self, event):
        if self.cap.isOpened():
            self.cap.release()
        event.accept()
