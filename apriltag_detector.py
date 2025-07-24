import cv2
import apriltag
from camera_stream import get_camera_frame
from utils import draw_detections

def main():
    detector = apriltag.Detector()

    while True:
        frame = get_camera_frame()
        if frame is None:
            continue

        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        detections = detector.detect(gray)

        frame_with_detections = draw_detections(frame, detections)

        cv2.imshow("AprilTag Detection", frame_with_detections)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
