import math
import mediapipe as mp
import numpy as np

class GestureRecognizer:
    """
    Classe responsável por reconhecer gestos da mão e convertê-los em comandos do mouse.
    Utiliza os landmarks detectados pelo MediaPipe para identificar diferentes posições dos dedos
    e classificá-las em gestos específicos.
    """

    # Constantes que definem os diferentes gestos reconhecidos
    MOUSE_BUTTONS_UP = 0    
    MOUSE_RIGHT_DOWN = 1   
    MOUSE_LEFT_DOWN = 2     
    SCROLL_UP = 3         
    SCROLL_DOWN = 4       

    def __init__(self):
        """
        Inicializa o reconhecedor de gestos.
        Define variáveis para suavização do cursor.
        """
        self.mp_hands = mp.solutions.hands
        self.cursor_smoothing_factor = 0.8  # Fator de suavização do movimento do cursor
        self.prev_x_coordinate = 0          # Coordenada X anterior para suavização
        self.prev_y_coordinate = 0          # Coordenada Y anterior para suavização

    def __get_distance(self, point1, point2):
        """
        Calcula a distância euclidiana entre dois pontos.
        
        Args:
            point1: Primeiro ponto com coordenadas x,y
            point2: Segundo ponto com coordenadas x,y
            
        Returns:
            float: Distância entre os pontos
        """
        return math.sqrt((point1.x - point2.x)**2 + (point1.y - point2.y)**2)

    def __is_mouse_gesture(self, hand_landmarks):
        """
        Verifica se a posição da mão corresponde ao gesto de controle do mouse.
        O gesto é reconhecido quando o dedo indicador está levantado e os dedos anelar e mindinho estão dobrados.
        
        Args:
            hand_landmarks: Lista de pontos de referência da mão detectados
            
        Returns:
            bool: True se o gesto for reconhecido, False caso contrário
        """
        hand_landmarks = hand_landmarks[0]

        pinky_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_TIP]
        pinky_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_MCP]

        ring_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP]
        ring_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_MCP]

        index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        index_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_MCP]

        return pinky_tip.y > pinky_mcp.y and ring_tip.y > ring_mcp.y and index_tip.y < index_mcp.y

    def __is_mouse_left_down(self, hand_landmarks):
        """
        Verifica se o gesto corresponde ao clique do botão esquerdo do mouse.
        O gesto é reconhecido quando a distância entre a ponta do polegar e do indicador é pequena.
        
        Args:
            hand_landmarks: Lista de pontos de referência da mão detectados
            
        Returns:
            bool: True se o gesto for reconhecido, False caso contrário
        """
        hand_landmarks = hand_landmarks[0]

        thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
        index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]

        distance_thumb_index = self.__get_distance(thumb_tip, index_tip)
        return distance_thumb_index < 0.08
    
    def __is_mouse_right_down(self, hand_landmarks):
        """
        Verifica se o gesto corresponde ao clique do botão direito do mouse.
        O gesto é reconhecido quando a distância entre a ponta do polegar e do dedo médio é pequena.
        
        Args:
            hand_landmarks: Lista de pontos de referência da mão detectados
            
        Returns:
            bool: True se o gesto for reconhecido, False caso contrário
        """
        hand_landmarks = hand_landmarks[0]

        thumb_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.THUMB_TIP]
        middle_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]

        distance_thumb_index = self.__get_distance(thumb_tip, middle_tip)
        return distance_thumb_index < 0.08

    def get_pointer_coordinates(self, hand_landmarks):
        """
        Obtém as coordenadas normalizadas do cursor baseadas na posição da mão.
        Aplica suavização ao movimento para evitar tremulações.
        
        Args:
            hand_landmarks: Lista de pontos de referência da mão detectados
            
        Returns:
            dict: Dicionário com as coordenadas x e y normalizadas do cursor

        TODO: Considerar mover a lógica de suavizar o cursor para fora dessa classe, já que sai do escopo de "Reconhecer gestos".
        """
        hand_landmarks = hand_landmarks[0]

        ring_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_MCP]

        smoother_x_coordinate = self.prev_x_coordinate * self.cursor_smoothing_factor + ring_mcp.x * (1 - self.cursor_smoothing_factor)
        smoother_y_coordinate = self.prev_y_coordinate * self.cursor_smoothing_factor + ring_mcp.y * (1 - self.cursor_smoothing_factor)

        self.prev_x_coordinate = smoother_x_coordinate
        self.prev_y_coordinate = smoother_y_coordinate

        return {'x': smoother_x_coordinate, 'y': smoother_y_coordinate}
    

    def __is_scroll_gesture(self, hand_landmarks):
        """
        Verifica se o gesto corresponde ao controle de scroll.
        O gesto é reconhecido quando o mindinho está dobrado e os dedos indicador, médio e anelar estão levantados.
        
        Args:
            hand_landmarks: Lista de pontos de referência da mão detectados
            
        Returns:
            bool: True se o gesto for reconhecido, False caso contrário
        """
        hand_landmarks = hand_landmarks[0]

        pinky_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_TIP]
        pinky_pip = hand_landmarks.landmark[self.mp_hands.HandLandmark.PINKY_PIP]

        index_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_TIP]
        index_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.INDEX_FINGER_MCP]

        middle_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        middle_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_MCP]

        ring_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_TIP]
        ring_mcp = hand_landmarks.landmark[self.mp_hands.HandLandmark.RING_FINGER_MCP]

        return pinky_tip.y > pinky_pip.y and ring_tip.y < ring_mcp.y and index_tip.y < index_mcp.y and middle_tip.y < middle_mcp.y

    def __is_scroll_up(self, hand_landmarks):
        """
        Verifica se o gesto de scroll indica movimento para cima.
        A direção é determinada pela posição do dedo médio em relação à sua articulação.
        
        Args:
            hand_landmarks: Lista de pontos de referência da mão detectados
            
        Returns:
            bool: True se o gesto indicar scroll para cima, False caso contrário
        """
        hand_landmarks = hand_landmarks[0]

        middle_tip = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_TIP]
        middle_pip = hand_landmarks.landmark[self.mp_hands.HandLandmark.MIDDLE_FINGER_PIP]

        return middle_tip.y < middle_pip.y

    def recognize(self, hand_landmarks):
        """
        Método principal que identifica qual gesto está sendo realizado.
        
        Args:
            hand_landmarks: Lista de pontos de referência da mão detectados
            
        Returns:
            int: Constante que identifica o gesto reconhecido
        """
        if(self.__is_mouse_gesture(hand_landmarks)):
            if(self.__is_mouse_left_down(hand_landmarks)):
                return self.MOUSE_LEFT_DOWN
            elif(self.__is_mouse_right_down(hand_landmarks)):
                return self.MOUSE_RIGHT_DOWN
            else:
                return self.MOUSE_BUTTONS_UP
        elif(self.__is_scroll_gesture(hand_landmarks)):
            if(self.__is_scroll_up(hand_landmarks)):
                return self.SCROLL_UP
            else:
                return self.SCROLL_DOWN
