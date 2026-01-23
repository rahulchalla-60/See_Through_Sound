import cv2
from config import CAMERA_INDEX, WINDOW_NAME

class CameraManager:
    def __init__(self):
        self.cap = cv2.VideoCapture(CAMERA_INDEX)
        cv2.namedWindow(WINDOW_NAME)
    
    def read_frame(self):
        return self.cap.read()
    
    def show_frame(self, frame):
        cv2.imshow(WINDOW_NAME, frame)
    
    def check_exit(self):
        # Check for 'q' key or window close
        if cv2.waitKey(1) & 0xFF == ord('q'):
            return True
        if cv2.getWindowProperty(WINDOW_NAME, cv2.WND_PROP_VISIBLE) < 1:
            return True
        return False
    
    def release(self):
        self.cap.release()
        cv2.destroyAllWindows()