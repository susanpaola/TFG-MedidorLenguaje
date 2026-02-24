# negocio/entities/transcription.py
from dataclasses import dataclass
from datetime import datetime

@dataclass
class Transcription:
    file_original: str
    file_audio: str
    transcription_txt: str
    transcription_pdf: str
    created_at: datetime = field(default_factory=datetime.utcnow)
