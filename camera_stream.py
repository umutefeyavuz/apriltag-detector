import cv2

def get_camera_frame(index=0):
    if not hasattr(get_camera_frame, "cap"):
        get_camera_frame.cap = cv2.VideoCapture(index)

    ret, frame = get_camera_frame.cap.read()
    if not ret:
        return None
    return frame
