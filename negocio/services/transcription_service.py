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

def transcribe_segments(audio_segments: List[str], language: str = None) -> str:
    """
    Transcribe una lista de segmentos y concatena el texto.
    """
    transcription = []
    for seg in audio_segments:
        # result es dict con 'text', 'segments'...
        result = model.transcribe(seg, language=language) if language else model.transcribe(seg)
        text = result.get("text", "").strip()
        if text:
            transcription.append(text)
    return "\n".join(transcription)
