#main.py
import speech_recognition as sr
import pyttsx3
from picamera2 import Picamera2, Preview
import time
from final_obstacl_avoidnce import main as avoid_obstacle
from image_captioning_final import main as predict_caption
from final_ocr import extract_text_from_scene

# Initialize the recognizer and the TTS engine
r = sr.Recognizer()
engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    # Get list of microphone names
    mic_list = sr.Microphone.list_microphone_names()

    # Let the user choose a microphone
    speak("Available microphones are:")
    for i, microphone_name in enumerate(mic_list):
        speak(f"{i}. {microphone_name}")
        print(f"{i}. {microphone_name}")
    speak("Please say the number of the microphone you want to use.")
    print("mic")
    mic_number = int(input())

    # Use the selected microphone
    with sr.Microphone(device_index=mic_number) as source:
        audio = r.listen(source)
        text = r.recognize_google(audio)
        return text


def capture_image(image_path):
    picam2 = Picamera2()
    camera_config = picam2.create_still_configuration(main={"size": (1920, 1080)}, lores={"size": (640, 480)}, display="lores")
    picam2.configure(camera_config)
    picam2.start()
    time.sleep(2)
    picam2.capture_file(image_path)

def main():
    speak("Please select an option:")
    speak("1. Extract text from scene")
    speak("2. Avoid obstacle")
    speak("3. Predict image caption")
    print("here")
    choice = listen()

    speak("capturing image")
    time.sleep(0.5)
    
    image_path = '/home/austine/Desktop/final_proj/downloads/a.jpg'
    capture_image(image_path)

    if choice == '1':
        result = extract_text_from_scene(image_path)
        print(result)
        speak(result)
    elif choice == '2':
        avoid_obstacle()
        # speak("Obstacle avoided.")
    elif choice == '3':
        result = predict_caption(image_path)
        print(result)
        speak(result)
    else:
        speak("Invalid choice. Please say 1, 2, or 3.")

if __name__ == "__main__":
    speak("initializing please wait")
    main()
