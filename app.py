import os
import subprocess
from flask import Flask, request, jsonify, render_template, send_file
from modules.audio_extractor import extract_audio
from modules.audio_converter import split_audio
from modules.transcriber import transcribe_audio
from modules.transcription_saver import save_transcription

app = Flask(__name__)
UPLOAD_FOLDER = "uploads"
TRANSCRIPTIONS_FOLDER = "transcriptions"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TRANSCRIPTIONS_FOLDER, exist_ok=True)

def convert_audio_to_wav(input_path, output_path):
    """Convierte cualquier archivo de audio a WAV con una frecuencia de muestreo estándar."""
    command = [
        "ffmpeg", "-i", input_path, "-ac", "1", "-ar", "16000", "-c:a", "pcm_s16le", output_path
    ]
    subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)

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

    # Guardar el archivo en la carpeta uploads
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    if file.filename.lower().endswith(('.mp4', '.avi', '.mov', '.mkv')):
        # Si es un video, extraemos el audio
        audio_path = os.path.join(UPLOAD_FOLDER, "audio.wav")
        extract_audio(file_path, audio_path)
    elif file.filename.lower().endswith(('.mp3', '.flac', '.aac', '.ogg', '.m4a', '.opus', '.wav')):
        # Si es un audio, lo convertimos a formato WAV estándar
        audio_path = os.path.join(UPLOAD_FOLDER, "converted_audio.wav")
        convert_audio_to_wav(file_path, audio_path)
    else:
        return jsonify({"error": "Formato de archivo no compatible."})

    # Dividir el audio en segmentos
    audio_segments = split_audio(audio_path)

    # Transcribir el audio
    transcripcion = transcribe_audio(audio_segments)

    # Guardar la transcripción en un archivo
    transcripcion_file = os.path.join(TRANSCRIPTIONS_FOLDER, f"{file.filename}.txt")
    save_transcription(transcripcion, transcripcion_file)

    return jsonify({"archivo": transcripcion_file})

@app.route("/descargar")
def descargar():
    file_path = request.args.get("file")
    if not file_path or not os.path.exists(file_path):
        return "Archivo no encontrado", 404
    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
