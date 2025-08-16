import cv2
import mediapipe as mp

class Camera:
    def __init__(self, min_confidence=0.7):
        self.cap = cv2.VideoCapture(0)
        self.mp_face_detection = mp.solutions.face_detection
        self.face_detection = self.mp_face_detection.FaceDetection(min_detection_confidence=min_confidence)
        self.raw_frame = None
        self.display_frame = None

    def get_frame(self):
        ret, frame = self.cap.read()
        if not ret:
            return None, None
        
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        self.raw_frame = rgb_frame.copy()
        self.display_frame = rgb_frame.copy()

        results = self.face_detection.process(rgb_frame)
        if results.detections:
            for detection in results.detections:
                bboxC = detection.location_data.relative_bounding_box
                ih, iw, _ = self.display_frame.shape
                x = int(bboxC.xmin * iw)
                y = int(bboxC.ymin * ih)
                w = int(bboxC.width * iw)
                h = int(bboxC.height * ih)

                cv2.rectangle(self.display_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                cv2.putText(self.display_frame, "Face Detected!", (x, y - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        return self.raw_frame, self.display_frame

    def release(self):
        self.cap.release()
