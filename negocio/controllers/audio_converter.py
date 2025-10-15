import os
import subprocess

def split_audio(audio_path):
    segments_folder = os.path.join(os.path.dirname(audio_path), "segments")
    os.makedirs(segments_folder, exist_ok=True)
    command = [
        "ffmpeg", "-i", audio_path, "-f", "segment", "-segment_time", "300",
        "-c", "copy", os.path.join(segments_folder, "chunk_%03d.wav")
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return sorted([os.path.join(segments_folder, f) for f in os.listdir(segments_folder) if f.endswith(".wav")])
