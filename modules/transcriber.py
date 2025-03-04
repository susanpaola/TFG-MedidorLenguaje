import whisper

class Transcriber:
    def __init__(self, model_size="base"):
        self.model = whisper.load_model(model_size)  # Carga el modelo una vez
    
    def transcribir_whisper(self, audio_path: str) -> str:
        result = self.model.transcribe(audio_path)
        return result["text"]

# Ejemplo de uso:
transcriber = Transcriber()  # Carga el modelo una vez
texto = transcriber.transcribir_whisper("uploads/audio.wav")
print(texto)
