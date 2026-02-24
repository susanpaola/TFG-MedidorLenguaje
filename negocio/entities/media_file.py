from dataclasses import dataclass
from datetime import datetime

@dataclass
class MediaFile:
    """
    Entidad que representa un archivo multimedia subido por el usuario.
    Puede ser audio o vídeo.
    """
    original_name: str           # nombre original del archivo
    stored_name: str             # nombre almacenado en el sistema
    media_type: str              # audio | video
    extension: str               # .mp3, .mp4, etc.
    content_hash: str            # hash para identificar contenido único
    duration_seconds: float      # duración total del archivo
    upload_date: datetime        # fecha de subida
    file_path: str               # ruta absoluta o relativa del archivo