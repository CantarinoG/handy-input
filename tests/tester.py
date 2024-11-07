import os
import cv2
import mediapipe as mp

class Tester:

    def __init__(self, gesture_recognizer):
        self.gesture_recognizer = gesture_recognizer
        self.dataset = []
        self.mp_hands = mp.solutions.hands
        self.hands = self.mp_hands.Hands(
            model_complexity=0,
            max_num_hands=1,
            min_detection_confidence=0.6,
            min_tracking_confidence=0.8
        )
        return
    
    def load_images(self, folder, label):
        for filename in os.listdir(folder):
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(folder, filename)
                self.dataset.append({
                    'image_path': image_path,
                    'real_label': label,
                    'detected_label': -1,
                })

    def classify_images(self):
        counter = 1
        for data in self.dataset:

            print(f'Processing {counter}/{len(self.dataset)}...')
            counter += 1

            image = cv2.imread(data['image_path'])
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            results = self.hands.process(image)

            if results.multi_hand_landmarks:
                hand_landmarks = results.multi_hand_landmarks
                gesture = self.gesture_recognizer.recognize(hand_landmarks)
                data['detected_label'] = gesture

    def get_detection_accuracy(self):
        detected = 0
        for data in self.dataset:
            if data['detected_label'] != -1:
                detected += 1
        return detected/len(self.dataset)
    
    def get_detection_accuracy_by_gesture(self, label):
        detected = 0
        total = 0
        for data in self.dataset:
            if data['real_label'] == label:
                total += 1
                if data['detected_label'] == label:
                    detected += 1
        return detected/total

    def get_gesture_accuracy(self):
        right_gestures = 0
        detected_hands = 0
        for data in self.dataset:
            if data['detected_label'] != -1:
                detected_hands += 1
                if data['real_label'] == data['detected_label']:
                    right_gestures += 1
        return right_gestures/detected_hands
    
    def get_detected_precision(self, label):
        true_positives = 0
        false_positives = 0
        for data in self.dataset:
            if data['detected_label'] != -1:
                if data['real_label'] == label and data['detected_label'] == label:
                    true_positives += 1
                elif data['real_label'] != label and data['detected_label'] == label:
                    false_positives += 1
        return true_positives / (true_positives + false_positives)
    
    def get_detected_recall(self, label):
        true_positives = 0
        false_negatives = 0
        for data in self.dataset:
            if data['detected_label'] != -1:
                if data['real_label'] == label and data['detected_label'] == label:
                    true_positives += 1
                elif data['real_label'] == label and data['detected_label'] != label:
                    false_negatives += 1
        return true_positives / (true_positives + false_negatives)
                
    def get_detected_f1_score(self, label):
        precision = self.get_detected_precision(label)
        recall = self.get_detected_recall(label)
        score = 2 * ((precision * recall)/(precision + recall))
        return score
