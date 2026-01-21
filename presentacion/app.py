# presentacion/app.py
import os
from flask import Flask, request, jsonify, render_template, send_file, current_app
from werkzeug.utils import secure_filename
from pathlib import Path
from fpdf import FPDF

from negocio.services.audio_service import (
    ensure_dirs, secure_unique_filename,
    extract_audio_from_video, convert_to_wav, split_audio, UPLOADS_DIR
)
from negocio.services.transcription_service import transcribe_segments

# Config
app = Flask(__name__, template_folder="templates", static_folder="static")
UPLOAD_FOLDER = UPLOADS_DIR
TRANSCRIPTIONS_FOLDER = os.path.abspath("transcriptions")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(TRANSCRIPTIONS_FOLDER, exist_ok=True)

ALLOWED_AUDIO_EXT = ('.mp3', '.flac', '.aac', '.ogg', '.m4a', '.opus', '.wav')
ALLOWED_VIDEO_EXT = ('.mp4', '.avi', '.mov', '.mkv', '.webm')

@app.route("/")
def index():
    return render_template("index.html")

def save_txt(text: str, dest_path: str):
    with open(dest_path, "w", encoding="utf-8") as f:
        f.write(text)

def save_pdf(text: str, dest_path: str):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.set_font("Arial", size=12)
    # dividir en lineas manejables
    for line in text.split("\n"):
        pdf.multi_cell(0, 7, line)
    pdf.output(dest_path)

@app.route("/transcribir", methods=["POST"])
def transcribir():
    if "file" not in request.files:
        return jsonify({"error": "No se envio archivo."}), 400

    file = request.files["file"]
    if file.filename == "":
        return jsonify({"error": "Nombre de archivo vacio."}), 400

    # Guardar con nombre seguro y unico
    original_filename = secure_unique_filename(file.filename)
    saved_path = os.path.join(UPLOAD_FOLDER, original_filename)
    file.save(saved_path)

    # Determinar tipo y obtener audio wav
    suffix = Path(saved_path).suffix.lower()
    audio_path = os.path.join(UPLOAD_FOLDER, f"{Path(original_filename).stem}_audio.wav")

    try:
        if suffix in ALLOWED_VIDEO_EXT:
            extract_audio_from_video(saved_path, audio_path)
        elif suffix in ALLOWED_AUDIO_EXT:
            convert_to_wav(saved_path, audio_path)
        else:
            return jsonify({"error": "Formato no soportado."}), 400

        # split y transcribir
        segments = split_audio(audio_path)
        transcription_text = transcribe_segments(segments)

        # Guardar transcripcion .txt y .pdf
        base_name = Path(original_filename).stem
        txt_path = os.path.join(TRANSCRIPTIONS_FOLDER, f"{base_name}.txt")
        pdf_path = os.path.join(TRANSCRIPTIONS_FOLDER, f"{base_name}.pdf")
        save_txt(transcription_text, txt_path)
        save_pdf(transcription_text, pdf_path)

        return jsonify({
            "txt": txt_path,
            "pdf": pdf_path,
            "message": "Transcripcion completada."
        })
    except Exception as e:
        current_app.logger.exception("Error durante la transcripcion")
        return jsonify({"error": str(e)}), 500

@app.route("/descargar")
def descargar():
    file_path = request.args.get("file")
    if not file_path or not os.path.exists(file_path):
        return "Archivo no encontrado", 404
    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True, port=5000)
