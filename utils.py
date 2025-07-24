import cv2

def draw_detections(frame, detections):
    for detection in detections:
        corners = detection.corners
        corners = [(int(p[0]), int(p[1])) for p in corners]

        for i in range(4):
            pt1 = corners[i]
            pt2 = corners[(i + 1) % 4]
            cv2.line(frame, pt1, pt2, (0, 255, 0), 2)

        center = (int(detection.center[0]), int(detection.center[1]))
        cv2.circle(frame, center, 5, (0, 0, 255), -1)

        tag_id = detection.tag_id
        cv2.putText(frame, f"ID: {tag_id}", (center[0] - 10, center[1] - 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
    return frame
