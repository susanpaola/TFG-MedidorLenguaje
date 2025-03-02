from flask import Flask, render_template, request, jsonify, send_file
from werkzeug.utils import secure_filename
import os

from modules.audio_extractor import AudioExtractor
from modules.audio_converter import AudioConverter
from modules.transcriber import Transcriber
from modules.transcription_saver import TranscriptionSaver

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
TRANSCRIPT_FOLDER = "transcriptions"

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TRANSCRIPT_FOLDER, exist_ok=True)

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/transcribir", methods=["POST"])
def transcribir():
    if "file" not in request.files:
        return jsonify({"error": "No se envió un archivo"}), 400
    
    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Nombre de archivo vacío"}), 400

    filename = secure_filename(file.filename)
    video_path = os.path.join(UPLOAD_FOLDER, filename)
    file.save(video_path)

    audio_path = os.path.join(UPLOAD_FOLDER, "audio.wav")
    AudioExtractor.extraer_audio(video_path, audio_path)
    AudioConverter.convertir_audio(audio_path, audio_path)

    texto = Transcriber.transcribir_whisper(audio_path)

    transcript_filename = f"{filename}.txt"
    transcript_path = os.path.join(TRANSCRIPT_FOLDER, transcript_filename)
    TranscriptionSaver.guardar_transcripcion(texto, transcript_path)

    return jsonify({
        "transcripcion": texto,
        "archivo": transcript_filename  # Devuelve el nombre del archivo para la descarga
    })

@app.route("/descargar/<filename>")
def descargar_transcripcion(filename):
    transcript_path = os.path.join(TRANSCRIPT_FOLDER, filename)
    return send_file(transcript_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
