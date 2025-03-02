from moviepy.editor import VideoFileClip

class AudioExtractor:
    @staticmethod
    def extraer_audio(video_path: str, audio_path: str):
        video = VideoFileClip(video_path)
        video.audio.write_audiofile(audio_path)
