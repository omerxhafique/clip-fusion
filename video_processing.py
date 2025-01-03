# video_processing.py

from moviepy.editor import VideoFileClip
from moviepy.video.fx.all import resize
import os
import multiprocessing as mp

def resize_to_portrait(chunk, target_height=1920):
    """
    Resize the video chunk to portrait mode for TikTok reels (9:16 aspect ratio).

    :param chunk: The video chunk to resize.
    :param target_height: The target height of the video in portrait mode.
    :return: The resized and cropped video chunk.
    """
    # Get current dimensions
    width, height = chunk.size
    
    # Calculate target width for a 9:16 aspect ratio
    aspect_ratio = 9 / 16
    target_width = int(target_height * aspect_ratio)
    
    # Resize the video chunk
    resized_chunk = resize(chunk, height=target_height)
    
    # Crop the video chunk to fit the portrait mode if needed
    x_center = resized_chunk.w / 2
    y_center = resized_chunk.h / 2
    crop_width = target_width
    crop_height = target_height

    cropped_chunk = resized_chunk.crop(x_center=x_center, y_center=y_center,
                                       width=crop_width, height=crop_height)
    
    return cropped_chunk

def process_chunk(start_time, end_time, video_path, output_dir, chunk_index):
    """
    Process and save a video chunk.

    :param start_time: Start time of the chunk.
    :param end_time: End time of the chunk.
    :param video_path: Path to the video file.
    :param output_dir: Directory where chunks will be saved.
    :param chunk_index: Index of the chunk.
    """
    # Load the video file within the worker process
    video = VideoFileClip(video_path)
    
    # Extract the chunk
    chunk = video.subclip(start_time, end_time)
    
    # Resize the chunk to portrait mode
    chunk = resize_to_portrait(chunk)
    
    # Define the output path for the chunk
    chunk_filename = os.path.join(output_dir, f"chunk_{chunk_index + 1}.mp4")
    try:
        chunk.write_videofile(chunk_filename, codec="libx264", audio_codec="aac", threads=4, preset='fast')
        print(f"Saved chunk {chunk_index + 1} to {chunk_filename}")
    except Exception as e:
        print(f"Error saving chunk {chunk_index + 1}: {e}")
    finally:
        # Release resources
        chunk.close()
        video.close()
 
def trim_video_to_chunks(video_path, output_dir, chunk_length=60):
    """
    Trims a video into chunks of specified length, resizes them to portrait mode, and saves them in the specified output directory.

    :param video_path: Path to the local video file.
    :param output_dir: Directory where chunks will be saved.
    :param chunk_length: Duration of each chunk in seconds.
    """
    # Ensure the output directory exists
    os.makedirs(output_dir, exist_ok=True)

    # Get video duration
    with VideoFileClip(video_path) as video:
        duration = video.duration
        num_chunks = int(duration // chunk_length) + (duration % chunk_length > 0)

    # Create a pool of workers for parallel processing
    pool = mp.Pool(processes=mp.cpu_count())
    
    # Prepare arguments for each chunk
    tasks = [(i * chunk_length, min((i + 1) * chunk_length, duration), video_path, output_dir, i) for i in range(num_chunks)]
    
    # Process chunks in parallel
    pool.starmap(process_chunk, tasks)
    
    # Close the pool
    pool.close()
    pool.join()
