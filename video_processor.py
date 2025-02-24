import subprocess
import os

class VideoProcessor:
    """Clase para extraer audio de un video usando FFmpeg."""
    
    def __init__(self, video_path):
        self.video_path = video_path
        self.audio_path = "audio_temp.mp3"  # Archivo temporal de audio
    
    def extract_audio(self):
        """Extrae el audio del video usando FFmpeg."""
        command = f"ffmpeg -i \"{self.video_path}\" -q:a 0 -map a \"{self.audio_path}\" -y"
        subprocess.run(command, shell=True, check=True)
        return self.audio_path
    
    def cleanup(self):
        """Elimina el archivo de audio temporal después de la transcripción."""
        if os.path.exists(self.audio_path):
            os.remove(self.audio_path)
