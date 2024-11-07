import cv2
import os
import numpy as np
import time

def extract_frames(video_path, num_frames, output_folder):
    """
    Extrai frames de um arquivo de vídeo e os salva como imagens individuais.

    Esta função abre um arquivo de vídeo, extrai um número específico de frames 
    distribuídos uniformemente ao longo do vídeo e os salva como arquivos de imagem JPG.

    Args:
        video_path (str): Caminho para o arquivo de vídeo a ser processado
        num_frames (int): Número de frames a serem extraídos do vídeo
        output_folder (str): Diretório onde os frames extraídos serão salvos

    Os frames são salvos com nomes no formato: timestamp_XXXX_frame.jpg, onde:
    - timestamp é o momento da extração em segundos desde epoch
    - XXXX é o número sequencial do frame com 4 dígitos
    """
    os.makedirs(output_folder, exist_ok=True)
    
    cap = cv2.VideoCapture(video_path)
    
    total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
    
    if total_frames == 0:
        raise ValueError("Could not open video file or video file is empty")
    
    frame_indices = np.linspace(0, total_frames - 1, num_frames, dtype=int)
    
    timestamp = int(time.time())
    
    for idx, frame_no in enumerate(frame_indices):
        cap.set(cv2.CAP_PROP_POS_FRAMES, frame_no)
        
        ret, frame = cap.read()
        
        if ret:
            output_path = os.path.join(output_folder, f'{timestamp}_{idx:04d}_frame.jpg')
            cv2.imwrite(output_path, frame)
            
    cap.release()
