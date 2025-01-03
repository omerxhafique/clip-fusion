# audio_analysis.py

from moviepy.editor import VideoFileClip
from pydub import AudioSegment

def extract_audio(video_path):
    """
    Extracts audio from the video file and saves it as a .wav file.
    """
    video = VideoFileClip(video_path)
    audio_path = "temp_audio.wav"
    video.audio.write_audiofile(audio_path)
    return audio_path

def print_audio_levels(audio_path):
    """
    Prints the dBFS levels for the entire audio to help adjust the threshold.
    """
    audio = AudioSegment.from_wav(audio_path)
    print(f"Audio dBFS (loudness) range: {audio.dBFS}")

def detect_high_volume_segments(audio_path, threshold_db=-40.0, min_silence_len=1000):
    """
    Detects high volume segments in the audio file.

    :param audio_path: Path to the audio file.
    :param threshold_db: The volume threshold in decibels. Segments above this threshold are considered important.
    :param min_silence_len: The minimum length (in milliseconds) of silence to consider the end of an important segment.
    :return: A list of (start_time, end_time) tuples indicating important audio segments.
    """
    audio = AudioSegment.from_wav(audio_path)
    loud_segments = []
    
    start_time = None
    for ms in range(0, len(audio), 500):  # Analyze every 500 ms
        chunk = audio[ms:ms + 500]  # Get a 500 ms chunk
        if chunk.dBFS > threshold_db:
            if start_time is None:
                start_time = ms / 1000.0  # Convert to seconds
        else:
            if start_time is not None:
                end_time = ms / 1000.0
                if (end_time - start_time) * 1000 > min_silence_len:  # Ensure the segment is long enough
                    loud_segments.append((start_time, end_time))
                start_time = None

    return loud_segments