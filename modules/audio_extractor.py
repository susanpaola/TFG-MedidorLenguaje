import subprocess

def extraer_audio(video_path: str, audio_path: str):
    comando = [
        'ffmpeg', '-i', video_path, '-vn', '-acodec', 'mp3', audio_path, '-y'
    ]
    try:
        subprocess.run(comando, check=True)
        print(f"Audio extraído correctamente: {audio_path}")
    except subprocess.CalledProcessError as e:
        print(f"Error al extraer audio: {e}")