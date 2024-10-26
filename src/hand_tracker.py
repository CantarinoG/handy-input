import cv2
import mediapipe as mp
from gesture_recognizer import GestureRecognizer

class HandTracker:
    def __init__(self, gesture_recognizer, mouse_controller):
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.hands = self.mp_hands.Hands(
            model_complexity=1,
            max_num_hands=1,
            min_detection_confidence=0.8,
            min_tracking_confidence=0.8
        )
        self.cap = cv2.VideoCapture(0)
        self.gesture_recognizer = gesture_recognizer
        self.mouse_controller = mouse_controller

    def __show_debug_annotations(self, image, hand_landmarks):
        for hand_landmarks in hand_landmarks:
            self.mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            self.mp_hands.HAND_CONNECTIONS,
            self.mp_drawing_styles.get_default_hand_landmarks_style(),
            self.mp_drawing_styles.get_default_hand_connections_style())
    
    def __run_on_gesture(self, gesture, coordinates):
        coordinates.x = abs(1 - coordinates.x)
        if gesture == GestureRecognizer.MOUSE_BUTTONS_UP:
            self.mouse_controller.move_cursor(coordinates.x, coordinates.y)
            self.mouse_controller.buttons_up()
            print("mouse up")
        elif gesture == GestureRecognizer.MOUSE_LEFT_DOWN:
            self.mouse_controller.move_cursor(coordinates.x, coordinates.y)
            self.mouse_controller.left_button_down()
            print("left down")
        elif gesture == GestureRecognizer.MOUSE_RIGHT_DOWN:
            self.mouse_controller.move_cursor(coordinates.x, coordinates.y)
            self.mouse_controller.right_button_down()
            print("right down")
            

    def run(self, is_debug=False):
        while self.cap.isOpened():
          
            success, image = self.cap.read()

            if not success:
                print("No camera frame")
                continue
          
            image.flags.writeable = False
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = self.hands.process(image)

            if results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks
                gesture = self.gesture_recognizer.recognize(hand_landmarks)
                coordinates = self.gesture_recognizer.get_pointer_coordinates(hand_landmarks)
                self.__run_on_gesture(gesture, coordinates)

                if is_debug:
                    image.flags.writeable = True
                    self.__show_debug_annotations(image, hand_landmarks)

            if is_debug:
               image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
               cv2.imshow("Handy Input Debugger", cv2.flip(image, 1))
               if cv2.waitKey(1) & 0xFF == 27:
                    break
            
        self.cap.release()
