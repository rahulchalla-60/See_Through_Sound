from ultralytics import YOLO
from ultralytics.utils import LOGGER
import supervision as sv
from config import MODEL_PATH, CONFIDENCE_THRESHOLD

LOGGER.setLevel("ERROR")  # suppress YOLO logs

class Detector:
    def __init__(self):
        self.model = YOLO(MODEL_PATH)
    
    def detect(self, frame):
        results = self.model(frame, conf=CONFIDENCE_THRESHOLD)[0]
        detections = sv.Detections.from_ultralytics(results)
        return detections