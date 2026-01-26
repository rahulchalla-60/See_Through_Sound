from detector import Detector
from tracker import Tracker
from distance_calculator import estimate_distance
from position_analyzer import get_position
from annotator import Annotator
from camera_manager import CameraManager
from tts_announcer import TTSAnnouncer

def main():
    # Initialize components
    try:
        detector = Detector()
        tracker = Tracker()
        annotator = Annotator()
        camera = CameraManager()
        tts = TTSAnnouncer()
    except Exception as e:
        print(f"Failed to initialize: {e}")
        return
    
    frame_count = 0
    
    while True:
        ret, frame = camera.read_frame()
        if not ret:
            break

        frame_count += 1
        if frame_count < 10:
            continue

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
            
            # TTS announcement - only for valid and stable tracker IDs
            if track_id is not None and track_id >= 0:
                if distance:
                    announcement = f"{class_name} detected {position.lower()} at {distance:.1f} meters"
                else:
                    announcement = f"{class_name} detected {position.lower()}"
                tts.update_and_announce(track_id, announcement)

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