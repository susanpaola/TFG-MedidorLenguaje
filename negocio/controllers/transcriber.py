import whisper

def transcribe_audio(audio_segments):
    model = whisper.load_model("base")
    transcripcion = ""

    for segment in audio_segments:
        result = model.transcribe(segment)
        transcripcion += result["text"] + "\n"

    return transcripcion
