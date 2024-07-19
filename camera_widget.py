import cv2
import numpy as np
import mediapipe as mp
from PyQt5.QtCore import QTimer, pyqtSignal, Qt
from PyQt5.QtGui import QImage, QPixmap
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel
import math

class CameraWidget(QWidget):
    switch_page = pyqtSignal(list)

    def __init__(self):
        super().__init__()

        # Mediapipe 얼굴 검출 초기화
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(min_detection_confidence=0.2)

        # 웹캠 초기화
        self.cap = cv2.VideoCapture(0)

        # QLabel을 사용하여 웹캠 화면을 표시
        self.image_label = QLabel(self)
        self.image_label.setAlignment(Qt.AlignCenter)

        # 레이아웃 설정
        layout = QVBoxLayout()
        layout.addWidget(self.image_label)
        layout.setContentsMargins(0, 0, 0, 0)  # 여백 제거
        self.setLayout(layout)

        # CameraWidget 크기 설정
        self.setFixedSize(540, 960)

        # 타이머를 설정하여 주기적으로 웹캠 이미지를 업데이트
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_image)
        self.timer.start(30)  # 30ms마다 호출

        # 추적 상태를 위한 변수 초기화
        self.last_face_positions = None
        self.angle_within_range_start_time = None
        self.angle_threshold = 10
        self.position_threshold = 100
        self.required_duration = 3000  # milliseconds
        self.detected_faces = []

    def calculate_yaw_angle(self, detection):
        landmarks = detection.location_data.relative_keypoints

        # 왼쪽 눈, 오른쪽 눈, 코의 landmark 인덱스
        left_eye = landmarks[self.mp_face_detection.FaceKeyPoint.LEFT_EYE]
        right_eye = landmarks[self.mp_face_detection.FaceKeyPoint.RIGHT_EYE]
        nose = landmarks[self.mp_face_detection.FaceKeyPoint.NOSE_TIP]

        # 두 눈 중심점 계산
        eye_center_x = (left_eye.x + right_eye.x) / 2
        eye_center_y = (left_eye.y + right_eye.y) / 2

        # 코 좌표
        nose_x = nose.x
        nose_y = nose.y

        # 코를 기준으로 두 눈의 중심점 사이의 각도 계산
        angle_rad = math.atan2(eye_center_y - nose_y, eye_center_x - nose_x)
        angle_deg = math.degrees(angle_rad) + 90  # +90을 추가하여 기준을 맞춤

        return angle_deg

    def update_image(self):
        ret, frame = self.cap.read()
        if ret:
            # 웹캠 화면을 좌우 반전
            frame = cv2.flip(frame, 1)

            # Mediapipe로 얼굴 검출
            results = self.face_detection.process(frame)

            # 얼굴 검출 결과에 따라 박스 및 각도 표시
            face_detected = False
            current_face_positions = []
            box_color = (255, 0, 0)  # 빨간색 기본값
            if results.detections:
                for detection in results.detections:
                    bboxC = detection.location_data.relative_bounding_box
                    ih, iw, _ = frame.shape
                    bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                           int(bboxC.width * iw), int(bboxC.height * ih)
                    current_face_positions.append(bbox)

                    # 얼굴 각도 계산
                    yaw_angle = self.calculate_yaw_angle(detection)

                    # 얼굴 각도를 화면에 표시
                    cv2.putText(frame, f'Angle: {yaw_angle:.2f}', (bbox[0], bbox[1] - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)

                    if abs(yaw_angle) <= self.angle_threshold:
                        face_detected = True
                        box_color = (0, 255, 0)  # 초록색

                    # 얼굴 박스를 색상에 따라 그림
                    cv2.rectangle(frame, bbox, box_color, 2)

            # 얼굴 감지 및 조건 검사
            if face_detected and self.last_face_positions is not None:
                consistent_faces = len(current_face_positions) == len(self.last_face_positions)
                face_positions_consistent = all(
                    np.linalg.norm(np.array(cur_pos[:2]) - np.array(last_pos[:2])) < self.position_threshold
                    for cur_pos, last_pos in zip(current_face_positions, self.last_face_positions)
                )

                if consistent_faces and face_positions_consistent:
                    if self.angle_within_range_start_time is None:
                        self.angle_within_range_start_time = cv2.getTickCount()
                        self.detected_faces = []  # 초기화
                    else:
                        elapsed_time = (cv2.getTickCount() - self.angle_within_range_start_time) / cv2.getTickFrequency() * 1000
                        if elapsed_time >= self.required_duration:
                            # 얼굴 이미지를 저장
                            for detection in results.detections:
                                bboxC = detection.location_data.relative_bounding_box
                                ih, iw, _ = frame.shape
                                bbox = int(bboxC.xmin * iw), int(bboxC.ymin * ih), \
                                       int(bboxC.width * iw), int(bboxC.height * ih)
                                face_img = frame[bbox[1]:bbox[1]+bbox[3], bbox[0]:bbox[0]+bbox[2]]
                                self.detected_faces.append(face_img)
                            self.switch_page.emit(self.detected_faces)
                            self.angle_within_range_start_time = None
                else:
                    self.angle_within_range_start_time = None
            else:
                self.angle_within_range_start_time = None

            self.last_face_positions = current_face_positions

            # BGR 이미지를 RGB로 변환하여 QImage로 변환하여 QLabel에 표시
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = frame.shape
            q_image = QImage(frame.data, w, h, w * ch, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.image_label.setPixmap(pixmap)

    def stop_webcam(self):
        # 웹캠 타이머 정지
        self.timer.stop()

    def start_webcam(self):
        # 웹캠 타이머 시작
        self.timer.start(30)  # 30ms마다 호출

    def closeEvent(self, event):
        # 웹캠 리소스 해제
        if self.cap.isOpened():
            self.cap.release()
        event.accept()
