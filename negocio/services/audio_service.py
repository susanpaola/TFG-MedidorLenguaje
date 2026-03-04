# negocio/services/audio_service.py
from negocio.entities.audio_segment import AudioSegment

import os
import subprocess
import uuid

UPLOADS_DIR = os.path.abspath(os.path.join(os.getcwd(), "uploads"))

def ensure_dirs():
    os.makedirs(UPLOADS_DIR, exist_ok=True)

def secure_unique_filename(original_name: str) -> str:
    # crea nombre unico para evitar colisiones
    ext = os.path.splitext(original_name)[1]
    return f"{uuid.uuid4().hex}{ext}"

def extract_audio_from_video(video_path: str, output_audio_path: str):
    """
    Extrae audio de un video usando ffmpeg y produce WAV a 16k mono PCM.
    """
    command = [
        "ffmpeg", "-y", "-i", video_path, "-vn",
        "-acodec", "pcm_s16le", "-ar", "16000", "-ac", "1", output_audio_path
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)

def convert_to_wav(input_path: str, output_path: str):
    """
    Convierte cualquier audio soportado a WAV 16k mono PCM.
    """
    command = [
        "ffmpeg", "-y", "-i", input_path, "-ac", "1", "-ar", "16000",
        "-c:a", "pcm_s16le", output_path
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)

def split_audio(audio_path: str, segment_time: int = 300):
    """
    Divide audio en segmentos de `segment_time` segundos.
    Devuelve lista de entidades AudioSegment.
    """
    base_dir = os.path.dirname(audio_path)
    segments_folder = os.path.join(base_dir, "segments")
    os.makedirs(segments_folder, exist_ok=True)

    out_pattern = os.path.join(segments_folder, "chunk_%03d.wav")
    command = [
        "ffmpeg", "-y", "-i", audio_path, "-f", "segment",
        "-segment_time", str(segment_time), "-c", "copy", out_pattern
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)

    files = sorted([
        os.path.join(segments_folder, f)
        for f in os.listdir(segments_folder)
        if f.endswith(".wav")
    ])

    # Si no se generaron segmentos (archivo corto), devolver uno solo
    if not files:
        return [
            AudioSegment(
                segment_index=0,
                start_time=0.0,
                end_time=0.0,
                segment_path=audio_path
            )
        ]

    segments = []
    for idx, path in enumerate(files):
        segment = AudioSegment(
            segment_index=idx,
            start_time=idx * segment_time,
            end_time=(idx + 1) * segment_time,
            segment_path=path
        )
        segments.append(segment)

    return segments