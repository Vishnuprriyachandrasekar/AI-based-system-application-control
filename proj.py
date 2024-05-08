import cv2
import mediapipe as mp
import pyautogui
cam = cv2.VideoCapture(0)
face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()
ty=0
while True:
    _, frame = cam.read()
    frame = cv2.flip(frame, 1)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)
    landmark_points = output.multi_face_landmarks
    frame_h, frame_w, dimensions = frame.shape
    if landmark_points:
        landmarks = landmark_points[0].landmark
        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0))
            if id == 1:
                screen_x = screen_w / frame_w * x
                screen_y = screen_h / frame_h * y
                pyautogui.moveTo(screen_x, screen_y)
        left = [landmarks[145], landmarks[159]]
        for landmark in left:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 255))
        if (left[0].y - left[1].y) < 0.01:
            print("blink")
            ty=ty+1
            if ty>=3:
                cv2.destroyAllWindows() 
                break
            #pyautogui.click()
            #pyautogui.sleep(2)
        right = [landmarks[374], landmarks[386]]
        if (right[0].y - right[1].y) < 0.01:
            #pyautogui.rightClick()
            pyautogui.sleep(1)
    cv2.imshow('Eye Controlled Mouse', frame)
    cv2.waitKey(1)


import speech_recognition as sr
import pyautogui
import webbrowser
from sympy import sympify

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for commands...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        command = recognizer.recognize_google(audio).lower()
        print("You said:", command)
        return command
    except sr.UnknownValueError:
        print("Sorry, could not understand audio.")
        return None
    except sr.RequestError as e:
        print(f"Google API request failed; {e}")
        return None

def execute_command(command):
    if "scroll up" in command:
        pyautogui.scroll(3)
    elif "scroll down" in command:
        pyautogui.scroll(-3)
    elif "left click" in command:
        pyautogui.click()
    elif "right click" in command:
        pyautogui.rightClick()
    elif "open word" in command:
        pyautogui.hotkey("winleft")
        pyautogui.write("word")
        pyautogui.press("enter")
    elif "open file" in command:
        pyautogui.hotkey("winleft")
        pyautogui.write("file")
        pyautogui.press("enter")
    elif "type" in command:
        text_to_type = command.split("type", 1)[1].strip()
        pyautogui.write(text_to_type)
    elif "open browser" in command:
        webbrowser.open("https://www.google.com")  # Change the URL as needed
    elif "search" in command:
        search_query = command.split("search", 1)[1].strip()
        webbrowser.open(f"https://www.google.com/search?q={search_query}")
    elif "calculate" in command:
        perform_calculator_operations(command)
    elif "quit" in command or "exit" in command:
        exit()

def perform_calculator_operations(command):
    try:
        expression = command.split("calculate", 1)[1].strip()
        result = eval(expression)
        print("Result:", result)
        pyautogui.write(str(result))
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    while True:
        command = recognize_speech()
        if command:
            execute_command(command)

file
