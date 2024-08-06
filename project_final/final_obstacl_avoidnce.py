#final_obstacl_avoidnce.py
import cv2
import numpy as np
from ultralytics import YOLO
from ultralytics.utils.plotting import Annotator
from picamera2 import Picamera2
import matplotlib.pyplot as plt
from distance import setup, measure_distance
cv2.startWindowThread()

# Define model paths (replace with your downloaded files)
model_path = "yolov8n.pt"

def load_object_detector(model_path):
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

        left_objects = 0
        right_objects = 0
        for r in results:
            annotator = Annotator(frame)
            boxes = r.boxes
            for box in boxes:
                b = box.xyxy[0]  # get box coordinates in (left, top, right, bottom) format
                c = box.cls
                annotator.box_label(b, object_detector.names[int(c)])
                # Calculate distance to object

                            
                # Count objects in each half of the frame
                center_x = (b[0] + b[2]) / 2  # Calculate the center x-coordinate of the bounding box
                if center_x < frame.shape[1] / 2:  # If object is on the left side of the frame
                    left_objects += 1
                else:  # If object is on the right side of the frame
                    right_objects += 1

        # Provide navigation instructions based on the number of objects in each half of the frame
        if left_objects < right_objects:
            print("move left")
        elif right_objects < left_objects:
            print("move right")
        else:
            print("Equal space on both sides. Please move straight.")

        img = annotator.result() 
        if cv2.waitKey(1) == ord('q'):
                    break


def calculate_distance_to_object():
    
    setup()  # Initialize the GPIO pins
    distance = measure_distance() 
    return distance

def main():
    camera = Picamera2()
    object_detector = load_object_detector(model_path)
    while True:
        avoid_obstacle(camera, object_detector)
        if cv2.waitKey(1) == ord('q'):
            break
    camera.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
