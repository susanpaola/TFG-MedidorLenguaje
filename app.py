import os
from flask import Flask, request, jsonify, render_template
from modules.audio_extractor import extract_audio
from modules.audio_converter import split_audio
from modules.transcriber import transcribe_audio
from modules.transcription_saver import save_transcription

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
TRANSCRIPTIONS_FOLDER = "transcriptions"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TRANSCRIPTIONS_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/transcribir", methods=["POST"])
def transcribir():
    if "file" not in request.files:
        return jsonify({"error": "No se envió ningún archivo."})

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "No se seleccionó ningún archivo."})

    # Guardar video en la carpeta uploads
    video_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(video_path)

    # Extraer y dividir el audio
    audio_path = os.path.join(UPLOAD_FOLDER, "audio.wav")
    extract_audio(video_path, audio_path)
    audio_segments = split_audio(audio_path)

    # Transcribir el audio
    transcripcion = transcribe_audio(audio_segments)

    # Guardar la transcripción en un archivo
    transcripcion_file = os.path.join(TRANSCRIPTIONS_FOLDER, f"{file.filename}.txt")
    save_transcription(transcripcion, transcripcion_file)

    return jsonify({"transcripcion": transcripcion, "archivo": transcripcion_file})

if __name__ == "__main__":
    app.run(debug=True)
