import supervision as sv

class Annotator:
    def __init__(self):
        self.box_annotator = sv.BoxAnnotator(thickness=2)
        self.label_annotator = sv.LabelAnnotator(text_scale=0.6, text_thickness=2)
    
    def annotate(self, frame, detections, labels):
        frame = self.box_annotator.annotate(frame, detections)
        frame = self.label_annotator.annotate(frame, detections, labels)
        return frame