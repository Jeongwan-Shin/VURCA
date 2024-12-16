import os
import numpy as np
import av

import socket
def get_container_hostname():
    hostname = socket.gethostname()
    return hostname

def read_video_pyav(container, indices):
    frames = []
    container.seek(0)
    start_index = indices[0]
    end_index = indices[-1]
    for i, frame in enumerate(container.decode(video=0)):
        if i > end_index:
            break
        if i >= start_index and i in indices:
            frames.append(frame)
    return np.stack([x.to_ndarray(format="rgb24") for x in frames])

# Function to recursively search for the folder matching the video_id
def find_file_by_video_id(root_folder, video_id):
    for dirpath, dirnames, filenames in os.walk(root_folder):
        if video_id in filenames:
            return os.path.join(dirpath, video_id)
    return None

def video_load(video_path, vid):
    video_dir = find_file_by_video_id(video_path, str(vid) + ".mp4")    
    if not video_dir:
        raise FileNotFoundError(f"Video with ID {vid} not found in {video_path}")
    container = av.open(video_dir)
    total_frames = container.streams.video[0].frames
    indices = np.arange(0, total_frames, total_frames/32).astype(int)
    video = read_video_pyav(container, indices)
    return video

def FS_video_load(video_path, Qfs_idx, vid):
    video_dir = find_file_by_video_id(video_path, str(vid) + ".mp4")    
    if not video_dir:
        raise FileNotFoundError(f"Video with ID {vid} not found in {video_path}")
    container = av.open(video_dir)
    # total_frames = container.streams.video[0].frames
    indices = np.array(Qfs_idx).astype(int)
    video = read_video_pyav(container, indices)
    return video

def extract_frame_images(video_path, vid, target_frames=250):
    video_dir = find_file_by_video_id(video_path, str(vid) + ".mp4")
    if not video_dir:
        raise FileNotFoundError(f"Video with ID {vid} not found in {video_path}")
    
    container = av.open(video_dir)
    total_frames = container.streams.video[0].frames
    
    # Calculate indices to extract `target_frames` evenly
    if total_frames <= target_frames:
        # If total frames are fewer than the target, extract all frames
        indices = np.arange(0, total_frames).astype(int)
    else:
        # Otherwise, select `target_frames` indices uniformly
        indices = np.linspace(0, total_frames - 1, target_frames).astype(int)
        
    # Select frame indices at the specified interval
    #indices = np.arange(0, total_frames, interval).astype(int)
    # Extract frames at the specified indices
    video_frames = read_video_pyav(container, indices)
    
    return video_frames, indices

def extract_questions(text):
    # Split the text by newlines or specific delimiters to isolate questions
    lines = text.split("\n")
    questions = []
    
    for line in lines:
        # Identify lines that end with a question mark and strip extra spaces
        if "?" in line:
            questions.append(line.strip())
    
    return questions

def convert_to_serializable(obj):
    if isinstance(obj, np.ndarray):
        return obj.tolist()  # NumPy 배열 -> 리스트
    if isinstance(obj, (np.int64, np.int32)):
        return int(obj)  # NumPy 정수 -> Python 정수
    if isinstance(obj, (np.float64, np.float32)):
        return float(obj)  # NumPy 실수 -> Python 실수
    raise TypeError(f"Object of type {obj.__class__.__name__} is not JSON serializable")