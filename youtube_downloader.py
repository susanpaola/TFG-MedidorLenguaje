from pytube import YouTube

class YouTubeDownloader:
    """Clase para descargar videos de YouTube."""
    
    def __init__(self, url):
        self.url = url
        self.output_path = "downloaded_video.mp4"  # Nombre del video descargado
    
    def download_video(self):
        """Descarga un video de YouTube."""
        yt = YouTube(self.url)
        stream = yt.streams.filter(file_extension="mp4").first()
        stream.download(filename=self.output_path)
        print(f"\n✅ Video descargado como {self.output_path}")
        return self.output_path
