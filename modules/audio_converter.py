from pydub import AudioSegment

class AudioConverter:
    @staticmethod
    def convertir_audio(entrada: str, salida: str, formato: str = "wav"):
        audio = AudioSegment.from_file(entrada)
        audio.export(salida, format=formato)
