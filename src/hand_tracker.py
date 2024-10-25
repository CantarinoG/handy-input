import cv2
import mediapipe as mp

class HandTracker:
    def __init__(self):
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.hands = self.mp_hands.Hands(
            model_complexity=1,
            max_num_hands=1,
            min_detection_confidence=0.5,
            min_tracking_confidence=0.5
        )
        self.cap = cv2.VideoCapture(0)

    def __show_debug_annotations(self, image, hand_landmarks):
        for hand_landmarks in hand_landmarks:
            self.mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            self.mp_hands.HAND_CONNECTIONS,
            self.mp_drawing_styles.get_default_hand_landmarks_style(),
            self.mp_drawing_styles.get_default_hand_connections_style())
    

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

                if is_debug:
                    image.flags.writeable = True
                    self.__show_debug_annotations(image, hand_landmarks)

            if is_debug:
               image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
               cv2.imshow("Handy Tracker Debugger", cv2.flip(image, 1))
               if cv2.waitKey(1) & 0xFF == 27:
                    break
            
        self.cap.release()
