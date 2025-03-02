import ffmpeg

class AudioExtractor:
    @staticmethod
    def extraer_audio(video_path: str, audio_path: str):
        try:
            ffmpeg.input(video_path).output(audio_path, format='mp3', acodec='mp3').run(overwrite_output=True)
            print(f"Audio extraído correctamente: {audio_path}")
        except Exception as e:
            print(f"Error al extraer audio: {e}")
