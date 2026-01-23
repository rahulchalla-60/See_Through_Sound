from detector import Detector
from tracker import Tracker
from distance_calculator import estimate_distance
from position_analyzer import get_position
from annotator import Annotator
from camera_manager import CameraManager

def main():
    # Initialize components
    detector = Detector()
    tracker = Tracker()
    annotator = Annotator()
    camera = CameraManager()
    
    while True:
        ret, frame = camera.read_frame()
        if not ret:
            break

        h, w, _ = frame.shape

        # Detect objects
        detections = detector.detect(frame)
        
        # Track objects
        detections = tracker.update(detections)

        # Create labels with distance and position
        labels = []
        for box, cls_id, track_id in zip(
            detections.xyxy,
            detections.class_id,
            detections.tracker_id
        ):
            x1, y1, x2, y2 = box
            box_height = y2 - y1
            x_center = (x1 + x2) / 2

            distance = estimate_distance(box_height)
            position = get_position(x_center, w)

            class_name = detector.model.names[int(cls_id)]

            if distance:
                label = (
                    f"{class_name} #{track_id} | "
                    f"{position} | {distance:.2f}m"
                )
            else:
                label = f"{class_name} #{track_id} | {position}"

            labels.append(label)

        # Annotate frame
        frame = annotator.annotate(frame, detections, labels)

        # Show frame
        camera.show_frame(frame)

        # Check for exit
        if camera.check_exit():
            break

    camera.release()

if __name__ == "__main__":
    main()