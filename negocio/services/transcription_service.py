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

def transcribe_segments(audio_segments: List[AudioSegment], language: str = None) -> Transcription:
    """
    Transcribe una lista de AudioSegment y devuelve una entidad Transcription.
    """

    transcription_parts = []

    for seg in audio_segments:
        result = model.transcribe(seg.segment_path, language=language) if language else model.transcribe(seg.segment_path)
        text = result.get("text", "").strip()
        if text:
            transcription_parts.append(text)

    full_text = "\n".join(transcription_parts)

    # Creamos entidad (los paths se asignarán desde app.py)
    transcription = Transcription(
        file_original="",
        file_audio="",
        transcription_txt="",
        transcription_pdf="",
        created_at=datetime.utcnow()
    )

    # Guardamos temporalmente el texto dentro del txt
    transcription.transcription_txt = full_text

    return transcription