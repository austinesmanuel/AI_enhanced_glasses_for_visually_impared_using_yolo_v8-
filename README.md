# AI_enhanced_glasses_for_visually_impared_using_yolo_v8-
This is a project which shocase the software side for Ai featured glasses for visually imapred which has few fetaures lie path navigation, object detection, image description (sceanary description), and extract text from image (optical charecter recognition)
Here is a breakdown of all the used python files 
## final_obstacl_avoidnce.py
This program helps to navigate in an environment.It uses a camera feed to "see" objects. If something gets too close, it triggers a stop. Otherwise, it analyzes what it "sees" to find the most open space on either side. Based on this, it simulates moving the camera view (like navigating) towards the open space. It can even listen for a "stop" command to halt the simulation and provide voice feedback. This program essentially acts like a virtual navigation system for avoiding obstacles.

### Here is a deeper breakdown:
* Object Detection and YOLO Model:
    * This uses the YOLO (You Only Look Once) object detection model (specifically, YOLOv8n) to identify objects in real-time.
    * ***load_object_detector*** function initializes the YOLO model with the specified weights file (yolov8n.pt).
    * ***avoid_obstacle*** function captures frames from the camera and processes them using the YOLO model.
    * Detected objects are labeled on the frame, and their areas are calculated.

* Obstacle Avoidance Logic:
    * The system calculates the free space on the left and right sides based on detected objects.
    * If there’s more free space on one side, it instructs the robot to move in that direction.
    * If the free space is equal, it advises moving straight ahead.

* Speech Recognition and Stop Command:
    * The __listen_for_stop_command__ function continuously listens for voice commands:If the user says “stop,” the program terminates gracefully.

* Distance Measurement:
    * The **calculate_distance_to_object** function measures the distance to the detected object using the ultra sonic sensor from ***distance.py*** program file.

* Clean-Up and Exit:
    * The main function sets up the camera, starts the obstacle avoidance loop, and handles clean-up when the program exits.The **stop_program** flag ensures a controlled shutdown.The system also provides voice feedback (“exiting navigation”) when stopping.

* ***Features:***
    * Real-time object detection using YOLOv8n
    * Voice-controlled stop command
    * Dynamic obstacle avoidance logic
    * Distance measurement to detected objects

* ***Usage:***
    * Install necessary dependencies (OpenCV, Ultralytics, Picamera2, etc.).
    * Run the script (python obstacle_avoidance.py).
    * Speak “stop” to terminate the program.

## distance.py

This calculates distances using an ultrasonic sensor and provides real-time feedback.

* Components:
    * Ultrasonic Sensor (HC-SR04):
        * The HC-SR04 sensor emits ultrasonic waves and measures the time it takes for the waves to bounce back after hitting an object.
        * It consists of two main components: the transmitter (sends ultrasonic pulses) and the receiver (detects reflected waves).

    * GPIO Pins:
        * The script uses GPIO pins on the Raspberry Pi to interface with the ultrasonic sensor.
        * Specifically, it uses pins 23 (TRIG) for transmitting ultrasonic pulses and 24 (ECHO) for receiving reflected waves.

* Workflow:
    * Setup:
        * The `setup()` function initializes the GPIO mode and sets up the TRIG and ECHO pins.
        * It configures the pins as output (TRIG) and input (ECHO).

    * Distance Measurement:
        * The `measure_distance()` function continuously measures distances.
        * It triggers the ultrasonic sensor by sending a short pulse (10 microseconds) on the TRIG pin.
        * The sensor emits ultrasonic waves, which bounce off objects and return to the receiver.
        * The time between sending the pulse and receiving the echo (pulse duration) is measured.
        * Using the speed of sound (approximately 343 meters per second), the distance to the object is calculated:
            * Distance (in centimeters) = Pulse duration × 17150
            * The result is rounded to two decimal places.
        * The measured distance is printed to the console.

    * Clean-Up and Exit:
        * The script handles exceptions (e.g., KeyboardInterrupt) to ensure a graceful exit.
        * When the user interrupts the measurement (e.g., by pressing Ctrl+C), the program stops and cleans up GPIO resources.

* Usage:
    * Hardware Setup:
        * Connect the HC-SR04 sensor to the Raspberry Pi's GPIO pins (TRIG to pin 23, ECHO to pin 24).
        * Ensure proper power supply and ground connections.

    * Dependencies:
        * Install the necessary Python libraries (RPi.GPIO).

    * Run the Script:
        * Execute the script (`python distance.py`).
        * The program will continuously measure distances and display them in centimeters.
        * Press Ctrl+C to stop the measurement.

* Example Output:
```
Distance: 45.78 cm
```

Remember to adjust the GPIO pin numbers and any other settings based on your specific hardware configuration.
