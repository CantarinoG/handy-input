import math
import mediapipe as mp
import numpy as np

class GestureRecognizer:

    MOUSE_BUTTONS_UP = 0
    MOUSE_RIGHT_DOWN = 1
    MOUSE_LEFT_DOWN = 2

    def __init__(self):
        self.mp_hands = mp.solutions.hands

    def __get_distance(self, point1, point2):
        return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

    def __is_mouse_gesture(self, hand_landmarks):
        hand_landmarks = hand_landmarks[0]

        pinky_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_TIP]
        pinky_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_MCP]

        ring_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP]
        ring_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_MCP]

        index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        index_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_MCP]

        return pinky_tip.y > pinky_mcp.y and ring_tip.y > ring_mcp.y and index_tip.y < index_mcp.y

    def __is_mouse_left_down(self, hand_landmarks):
        hand_landmarks = hand_landmarks[0]

        thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
        index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]

        distance_thumb_index = self.__get_distance(thumb_tip, index_tip)
        return distance_thumb_index < 0.05
    
    def __is_mouse_right_down(self, hand_landmarks):
        hand_landmarks = hand_landmarks[0]

        thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
        middle_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

        distance_thumb_index = self.__get_distance(thumb_tip, middle_tip)
        return distance_thumb_index < 0.05

    def get_pointer_coordinates(self, hand_landmarks):
        hand_landmarks = hand_landmarks[0]

        ring_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_MCP]

        return ring_mcp
    

    def recognize(self, hand_landmarks):
        if(self.__is_mouse_gesture):
            if(self.__is_mouse_left_down(hand_landmarks)):
                return self.MOUSE_LEFT_DOWN
            elif(self.__is_mouse_right_down(hand_landmarks)):
                return self.MOUSE_RIGHT_DOWN
            else:
                return self.MOUSE_BUTTONS_UP

        
