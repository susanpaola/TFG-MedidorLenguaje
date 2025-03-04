import os
from flask import Flask, request, render_template, jsonify
from modules.audio_extractor import extraer_audio
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
    if 'file' not in request.files:
        return jsonify({"error": "No se ha subido ningún archivo"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "Nombre de archivo vacío"}), 400

    video_path = os.path.join(UPLOAD_FOLDER, "video.mp4")
    audio_path = os.path.join(UPLOAD_FOLDER, "audio.wav")
    transcript_path = os.path.join(TRANSCRIPT_FOLDER, "transcription.txt")

    file.save(video_path)

    try:
        # Extraer y convertir el audio
        extraer_audio(video_path, audio_path)
        AudioConverter.convertir_audio(audio_path, audio_path)

        # Transcribir el audio
        texto_transcrito = Transcriber.transcribir_whisper(audio_path)

        # Guardar la transcripción en un archivo
        TranscriptionSaver.guardar_transcripcion(texto_transcrito, transcript_path)

        # Devolver la transcripción al frontend
        return jsonify({"transcripcion": texto_transcrito, "archivo": transcript_path}), 200

    except Exception as e:
        return jsonify({"error": f"Error durante la transcripción: {str(e)}"}), 500

if __name__ == "__main__":
    app.run(debug=True)