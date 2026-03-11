from dataclasses import dataclass

"""
    La entidad representa la extraccion de audio a partir de un archivo multimedia.
    """

@dataclass
class AudioExtraction:
    
    channels: int                # número de canales (mono, estéreo)
    sample_rate: int             # frecuencia de muestreo (ej. 16000)
    format: str                  # formato del audio (wav, pcm, etc.)
    audio_path: str              # ruta del archivo de audio generado