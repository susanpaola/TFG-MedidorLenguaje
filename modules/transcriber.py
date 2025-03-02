import whisper

class Transcriber:
    @staticmethod
    def transcribir_whisper(audio_path: str) -> str:
        model = whisper.load_model("base")
        result = model.transcribe(audio_path)
        return result["text"]
