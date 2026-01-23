from config import KNOWN_PERSON_HEIGHT_M, FOCAL_LENGTH

def estimate_distance(box_height_px, real_height_m=KNOWN_PERSON_HEIGHT_M):
    if box_height_px <= 0:
        return None
    return (real_height_m * FOCAL_LENGTH) / box_height_px