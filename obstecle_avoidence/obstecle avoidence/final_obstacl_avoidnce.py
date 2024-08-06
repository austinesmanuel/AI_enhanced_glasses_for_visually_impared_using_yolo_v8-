import cv2
import numpy as np
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
from picamera2 import Picamera2
import matplotlib.pyplot as plt
cv2.startWindowThread()

# Define model paths (replace with your downloaded files)
model_path = "yolov8n.pt"

def load_object_detector(model_path):
    """
    Loads the YOLOv8 model using Ultralytics.

    Args:
        model_path: Path to the YOLOv8 model file (.pt).

    Returns:
        A loaded YOLO object from Ultralytics.
    """
    return YOLO(model_path)

def avoid_obstacle(picam, object_detector):
    picam.preview_configuration.main.size = (480, 480)
    picam.preview_configuration.main.format = "RGB888"
    picam.preview_configuration.main.align()
    picam.configure("preview")
    picam.start()
    while True:
        frame = picam.capture_array() # Capture a frame
        distance = calculate_distance_to_object()
        if (distance < 10):
             print("stop imidiatly!!!")
             continue
        elif (distance < 50):
            results = object_detector.predict(frame)  # Perform object detection
        else:
             continue
        left_area = 0
        right_area = 0
        total_area = frame.shape[0] * frame.shape[1]

        for r in results:
            annotator = Annotator(frame)
            boxes = r.boxes
            for box in boxes:
                b = box.xyxy[0]  # get box coordinates in (left, top, right, bottom) format
                c = box.cls
                annotator.box_label(b, object_detector.names[int(c)])

                # Calculate area of the bounding box
                box_area = (b[2] - b[0]) * (b[3] - b[1])

                # Calculate distance to object
                distance = calculate_distance_to_object(b, frame.shape)

                # Calculate areas on each half of the frame
                center_x = (b[0] + b[2]) / 2  # Calculate the center x-coordinate of the bounding box
                if center_x < frame.shape[1] / 2:  # If object is on the left side of the frame
                    left_area += box_area
                else:  # If object is on the right side of the frame
                    right_area += box_area

        # Calculate free space on each side of the frame
        left_free_space = total_area / 2 - left_area
        right_free_space = total_area / 2 - right_area

        # Provide navigation instructions based on the free space on each half of the frame
        if left_free_space > right_free_space:
            print("move left")
        elif right_free_space > left_free_space:
            print("move right")
        else:
            print("Equal space on both sides. Please move straight.")

            img = annotator.result() 
            # plt.imshow(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
            # plt.show()

            # cv2.imshow('YOLO V8 Detection', img)
            if cv2.waitKey(1) == ord('q'):
                        break

def calculate_distance_to_object():
    from distance import setup, measure_distance
    setup()  # Initialize the GPIO pins
    distance = measure_distance() 
    return distance

# Access camera
camera = Picamera2()  # Use Picamera2 instead of cv2.VideoCapture(0)

# Load YOLOv8 model
object_detector = load_object_detector(model_path)

while True:
    avoid_obstacle(camera, object_detector)
    if cv2.waitKey(1) == ord('q'):
        break

camera.release()  # Release resources
cv2.destroyAllWindows()
