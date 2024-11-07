import os
import cv2
import mediapipe as mp

class Tester:
    """
    Classe responsável por testar o reconhecimento de gestos em um conjunto de imagens.
    
    Esta classe carrega imagens de um ou mais diretórios, processa cada uma delas usando o 
    MediaPipe Hands e o GestureRecognizer, e calcula métricas de performance como
    acurácia, precisão, recall e F1-score.
    """

    def __init__(self, gesture_recognizer):
        """
        Inicializa o Tester com um reconhecedor de gestos.

        Args:
            gesture_recognizer: Instância de GestureRecognizer que será usada para classificar os gestos
        """
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
        """
        Carrega imagens de um diretório e as associa a um rótulo específico.

        Args:
            folder (str): Caminho para o diretório contendo as imagens
            label (int): Rótulo que será associado a todas as imagens do diretório
        """
        for filename in os.listdir(folder):
            if filename.endswith(('.png', '.jpg', '.jpeg')):
                image_path = os.path.join(folder, filename)
                self.dataset.append({
                    'image_path': image_path,
                    'real_label': label,
                    'detected_label': -1,
                })

    def classify_images(self):
        """
        Processa todas as imagens do dataset usando MediaPipe Hands e classifica os gestos.
        Para cada imagem, detecta landmarks da mão e usa o gesture_recognizer para determinar o gesto.
        """
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
        """
        Calcula a acurácia geral da detecção de mãos.

        Returns:
            float: Proporção de imagens onde uma mão foi detectada em relação ao total
        """
        detected = 0
        for data in self.dataset:
            if data['detected_label'] != -1:
                detected += 1
        return detected/len(self.dataset)
    
    def get_detection_accuracy_by_gesture(self, label):
        """
        Calcula a acurácia da detecção de mãos para um gesto específico.

        Args:
            label (int): Rótulo do gesto para calcular a acurácia

        Returns:
            float: Proporção de detecções corretas para o gesto específico
        """
        detected = 0
        total = 0
        for data in self.dataset:
            if data['real_label'] == label:
                total += 1
                if data['detected_label'] == label:
                    detected += 1
        return detected/total
    
    def get_detected_precision(self, label):
        """
        Calcula a precisão para um gesto específico considerando apenas mãos detectadas.

        Args:
            label (int): Rótulo do gesto para calcular a precisão

        Returns:
            float: Precisão do reconhecimento para o gesto específico
        """
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
        """
        Calcula o recall para um gesto específico considerando apenas mãos detectadas.

        Args:
            label (int): Rótulo do gesto para calcular o recall

        Returns:
            float: Recall do reconhecimento para o gesto específico
        """
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
        """
        Calcula o F1-score para um gesto específico considerando apenas mãos detectadas.

        Args:
            label (int): Rótulo do gesto para calcular o F1-score

        Returns:
            float: F1-score do reconhecimento para o gesto específico
        """
        precision = self.get_detected_precision(label)
        recall = self.get_detected_recall(label)
        score = 2 * ((precision * recall)/(precision + recall))
        return score
