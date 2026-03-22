# negocio/services/transcription_service.py

from datetime import datetime #Importanción de la biblioteca estandar
import whisper
from typing import List

#Importaciones de mi proyecto
from negocio.entities.audio_segment import AudioSegment
from negocio.entities.transcription import Transcription

# Cargar modelo globalmente al importar este modulo (evita recarga en cada peticion)

MODEL_NAME = "base" # aqui puedo cambiar por small, medium o large
print(f"[INFO] Cargando modelo Whisper '{MODEL_NAME}'... (esto tarda al inicio)")
model = whisper.load_model(MODEL_NAME)
print("[INFO] Modelo cargado.")

def transcribe_segments(audio_segments: List[str], language: str = None):
    """
    Transcribe audio segments and capture timestamps from Whisper.
    """

    transcription_text_parts = []
    speech_segments: List[AudioSegment] = []

    segment_counter = 0

    for seg in audio_segments:

        result = model.transcribe(seg, language=language) if language else model.transcribe(seg)

        text = result.get("text", "").strip()
        if text:
            transcription_text_parts.append(text)

        whisper_segments = result.get("segments", [])

        for ws in whisper_segments:

            speech_segment = AudioSegment(
                segment_index=segment_counter,
                start_time=ws.get("start", 0.0),
                end_time=ws.get("end", 0.0),
                text=ws.get("text", "").strip(),
                segment_path=seg
            )

            speech_segments.append(speech_segment)
            segment_counter += 1

    transcription_text = "\n".join(transcription_text_parts)

    return transcription_text, speech_segments