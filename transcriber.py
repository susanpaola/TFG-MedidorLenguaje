import whisper

class Transcriber:
    """Clase para transcribir audio a texto usando Whisper."""
    
    def __init__(self, model_type="medium"):
        self.model = whisper.load_model(model_type)
    
    def transcribe(self, audio_path):
        """Transcribe el audio a texto."""
        result = self.model.transcribe(audio_path, language="es")
        return result["text"]

    def save_transcription(self, text, output_file="transcription.txt"):
        """Guarda la transcripción en un archivo de texto."""
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(text)
        print(f"\n✅ Transcripción guardada en {output_file}")
