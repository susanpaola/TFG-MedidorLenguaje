from dataclasses import dataclass

"""
    Entidad que representa un segmento de audio generado tras la division.
    """

@dataclass
class AudioSegment:
    segment_index: int
    start_time: float
    end_time: float
    text: str
    segment_path: str