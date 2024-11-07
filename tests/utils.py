import cv2
import os
import numpy as np
import time

def extract_frames(video_path, num_frames, output_folder):

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
