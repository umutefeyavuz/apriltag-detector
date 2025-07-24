# AprilTag High FPS Detector

This lightweight Python project uses the `apriltag` library to detect AprilTags with high FPS performance. It avoids using YOLO or complex object detection frameworks and is optimized for low-power devices like the Raspberry Pi.

## Features

- High FPS AprilTag detection
- Minimal dependencies
- Clean, modular code

## How to Run

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
2. Run the detector:

python apriltag_detector.py

3. Press q to exit the display window.

Dependencies

    OpenCV (for image capture and drawing)

    NumPy

    Python apriltag bindings

    imutils

Notes

    Tested on Raspberry Pi 5 with a USB webcam

    Designed for real-time use in FRC and robotics projects