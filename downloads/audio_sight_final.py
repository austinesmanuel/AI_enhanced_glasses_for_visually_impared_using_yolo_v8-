import RPi.GPIO as gpio
from gtts import gTTS
import pytesseract as pya
from picamera2 import Picamera2
import os
import cv2
import time
import serial
import threading
import numpy as np

picam = Picamera2()
picam.preview_configuration.main.size = (480, 480)
picam.preview_configuration.main.format = "RGB888"
picam.preview_configuration.main.align()
picam.configure("preview")
picam.start()

help_btn = 16
obj_btn = 20
ocr_btn = 21
buz = 19
stat_led = 13

flag1=0
flag2=0
flag3=0
flag4=0

ser = serial.Serial(port='/dev/ttyS0', baudrate=9600, parity=serial.PARITY_NONE, stopbits=serial.STOPBITS_ONE, bytesize=serial.EIGHTBITS, timeout=1)

classesFile = '/home/pi/AUDIO_SIGHT/coco.names'
classNames = []
with open(classesFile, 'rt') as f:
    classNames = f.read().rstrip('\n').split('\n')

modelconfig = '/home/pi/AUDIO_SIGHT/yolov3tiny.cfg'
modelweight = '/home/pi/AUDIO_SIGHT/yolov3tiny.weights'
net = cv2.dnn.readNetFromDarknet(modelconfig, modelweight)


def main():
    global flag1,flag2,flag3,flag4
    gpio.setwarnings(False)
    gpio.setmode(gpio.BCM)
    gpio.setup(ocr_btn, gpio.IN)
    gpio.setup(obj_btn, gpio.IN)
    gpio.setup(help_btn, gpio.IN)
    gpio.setup(buz, gpio.OUT)
    gpio.setup(stat_led, gpio.OUT)
    threading.Thread(target=buffering).start()

    speak("Welcome to the Smart Assistive System for the Blind")
    print("Welcome to the Smart Assistive System for the Blind")
    while True:
        help_val = gpio.input(help_btn)
        obj_val = gpio.input(obj_btn)
        ocr_val = gpio.input(ocr_btn)

        if ocr_val == 0:
            flag1 = 1
        if ocr_val == 1 and flag1 == 1:
            flag1 = 0
            speak("System is going to read text")
            readText()

        if obj_val == 0:
            flag2 = 1
        if obj_val == 1 and flag2 == 1:
            flag2 = 0
            speak("System is going to detect objects in front of you")
            obj = detect()
            if obj is not None:
                obj = gTTS(text=obj + " detected in front of the camera.", lang='en', slow=False)
                obj.save("aud.mp3")
                os.system("sudo mpg321 aud.mp3")

        if help_val == 0:
            flag3 = 1
        if help_val == 1 and flag3 == 1:
            flag3 = 0
            ser.write('A'.encode())
            print("emergency")
            gpio.output(buz,True)
            time.sleep(1)
            gpio.output(buz,False)


def readText():
    try:
        print("System is reading your image. Please wait.")
        speak("System is reading your image. Please wait.")
        caps = cv2.VideoCapture(0)
        ocr_flag = 0
        while ocr_flag == 0:
            # Display camera preview for 5 seconds
            start_time = time.time()
            while time.time() - start_time < 5:
                frame = picam.capture_array()
                cv2.imshow('Live Detection', frame)
                cv2.waitKey(1)
            # Save the captured frame as an image
            cv2.imwrite("captured_image.jpg", frame)
            # Close all windows
            cv2.destroyAllWindows()
            frame = cv2.imread("captured_image.jpg")
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.bilateralFilter(gray, 11, 17, 17)
            text = pya.image_to_string(gray, config='')
            if text:
                print(text)
                speak(text)
                ocr_flag=1
    except Exception as e:
        print("Warning:", e)
        caps.release()
        cv2.destroyAllWindows()


def speak(text):
    myobj = gTTS(text=text, lang='en', slow=False)
    myobj.save("/home/pi/AUDIO_SIGHT/speech.mp3")
    os.system("mpg321 /home/pi/AUDIO_SIGHT/speech.mp3")


def detect():
    cap = cv2.VideoCapture(0)
    obj_flag = 0
    while obj_flag == 0:
        # Display camera preview for 5 seconds
        start_time = time.time()
        while time.time() - start_time < 5:
            img = picam.capture_array()
            cv2.imshow('Live Detection', img)
            cv2.waitKey(1)
        # Save the captured frame as an image
        cv2.imwrite("captured_image.jpg", img)
        # Close all windows
        cv2.destroyAllWindows()
        img = cv2.imread("captured_image.jpg")
        blob = cv2.dnn.blobFromImage(img, 1/255, (320, 320), [0, 0, 0], 1, crop=False)
        net.setInput(blob)
        layerNames = net.getLayerNames()
        a = net.getUnconnectedOutLayers()
        outputNames = [layerNames[i - 1] for i in net.getUnconnectedOutLayers()]
        outputs = net.forward(outputNames)
        h, w, c = img.shape
        bbox = []
        classids = []
        conf = []
        for output in outputs:
            for det in output:
                score = det[5:]
                classid = np.argmax(score)
                confidence = score[classid]
                if confidence > 0.4:
                    wd, ht = int(det[2] * w), int(det[3] * h)
                    x, y = int((det[0] * w) - wd / 2), int((det[1] * h) - ht / 2)
                    bbox.append([x, y, wd, ht])
                    classids.append(classid)
                    conf.append(float(confidence))
        indices = cv2.dnn.NMSBoxes(bbox, conf, 0.5, 0.3)
        for i in indices:
            i = i
            box = bbox[i]
            x, y, w, h = box[0], box[1], box[2], box[3]
            res=classNames[classids[i]]
            print(res)
            obj_flag = 1



def buffering():
    while True:
        gpio.output(stat_led,True)
        time.sleep(1)
        gpio.output(stat_led,False)
        time.sleep(1)
        

if __name__ == "__main__":
    main()
