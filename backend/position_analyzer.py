def get_position(x_center, frame_width):
    if x_center < frame_width * 0.33:
        return "LEFT"
    elif x_center > frame_width * 0.66:
        return "RIGHT"
    else:
        return "CENTER"