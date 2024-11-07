import cv2
import mediapipe as mp
from gesture_recognizer import GestureRecognizer

class HandTracker:
    """
    Classe responsável por rastrear a mão do usuário através da webcam e converter os gestos em comandos do mouse.
    Utiliza o MediaPipe para detectar os pontos de referência da mão e o GestureRecognizer para interpretar os gestos.
    """

    def __init__(self, gesture_recognizer, mouse_controller):
        """
        Inicializa o rastreador de mão.

        Args:
            gesture_recognizer: Instância de GestureRecognizer para reconhecimento dos gestos
            mouse_controller: Instância de MouseController para controle do mouse
        """
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils
        self.mp_drawing_styles = mp.solutions.drawing_styles
        self.hands = self.mp_hands.Hands(
            model_complexity=0,
            max_num_hands=1,
            min_detection_confidence=0.8,
            min_tracking_confidence=0.8
        )
        self.cap = cv2.VideoCapture(0)
        self.gesture_recognizer = gesture_recognizer
        self.mouse_controller = mouse_controller

    def __show_debug_annotations(self, image, hand_landmarks):
        """
        Desenha as anotações de debug na imagem, mostrando os landmarks e conexões da mão.

        Args:
            image: Frame da webcam onde as anotações serão desenhadas
            hand_landmarks: Lista de pontos de referência da mão detectados
        """
        for hand_landmarks in hand_landmarks:
            self.mp_drawing.draw_landmarks(
            image,
            hand_landmarks,
            self.mp_hands.HAND_CONNECTIONS,
            self.mp_drawing_styles.get_default_hand_landmarks_style(),
            self.mp_drawing_styles.get_default_hand_connections_style())
    
    def __run_on_gesture(self, gesture, coordinates):
        """
        Executa a ação correspondente ao gesto detectado.
        Inverte a coordenada X para corresponder ao movimento natural da mão (espelhado).

        Args:
            gesture: Constante que identifica o gesto reconhecido
            coordinates: Dicionário com as coordenadas x,y normalizadas do cursor
        """
        inverse_coordinate_x = abs(1 - coordinates['x'])
        
        if gesture == GestureRecognizer.MOUSE_BUTTONS_UP:
            self.mouse_controller.move_cursor(inverse_coordinate_x, coordinates['y'])
            self.mouse_controller.buttons_up()
            print("mouse up")
        elif gesture == GestureRecognizer.MOUSE_LEFT_DOWN:
            self.mouse_controller.move_cursor(inverse_coordinate_x, coordinates['y'])
            self.mouse_controller.left_button_down()
            print("left down")
        elif gesture == GestureRecognizer.MOUSE_RIGHT_DOWN:
            self.mouse_controller.move_cursor(inverse_coordinate_x, coordinates['y'])
            self.mouse_controller.right_button_down()
            print("right down")
        elif gesture == GestureRecognizer.SCROLL_UP:
            self.mouse_controller.scroll_up(1)
            print("scroll up")
        elif gesture == GestureRecognizer.SCROLL_DOWN:
            self.mouse_controller.scroll_down(1)
            print("scroll down")

    def run(self, is_debug=False):
        """
        Inicia o loop principal de rastreamento da mão.
        Captura frames da webcam, processa-os para detectar a mão e executa as ações correspondentes.
        
        Args:
            is_debug (bool): Se True, mostra uma janela com visualização da detecção da mão
        """
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
