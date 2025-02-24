import os
from youtube_downloader import YouTubeDownloader
from video_processor import VideoProcessor
from transcriber import Transcriber

def main(video_source, is_youtube=False, model="medium", output_file="transcription.txt"):
    """Función principal para procesar el video y obtener la transcripción."""
    
    if is_youtube:
        downloader = YouTubeDownloader(video_source)
        video_path = downloader.download_video()
    else:
        video_path = video_source  # Si el video ya está en la PC
    
    processor = VideoProcessor(video_path)
    audio_path = processor.extract_audio()
    
    transcriber = Transcriber(model)
    transcription_text = transcriber.transcribe(audio_path)
    
    transcriber.save_transcription(transcription_text, output_file)
    
    processor.cleanup()

def menu():
    """Menú interactivo para elegir cómo subir el video."""
    while True:
        print("\n🎙️ Bienvenido al Transcriptor de Videos")
        print("1️⃣ Subir un video desde la PC")
        print("2️⃣ Descargar un video desde YouTube")
        print("0️⃣ Salir")
        
        opcion = input("\nSelecciona una opción: ")

        if opcion == "1":
            video_path = input("\n🔍 Ingresa la ruta del video en tu PC: ").strip()
            if not os.path.exists(video_path):
                print("\n❌ Error: El archivo no existe.")
                continue
            
            model = input("\n🧠 Ingresa el modelo de Whisper (tiny, base, small, medium, large) [medium]: ").strip() or "medium"
            output_file = input("\n💾 Nombre del archivo de salida [transcription.txt]: ").strip() or "transcription.txt"
            
            print("\n🔄 Procesando el video...\n")
            main(video_path, is_youtube=False, model=model, output_file=output_file)

        elif opcion == "2":
            youtube_url = input("\n🔗 Ingresa la URL del video de YouTube: ").strip()
            model = input("\n🧠 Ingresa el modelo de Whisper (tiny, base, small, medium, large) [medium]: ").strip() or "medium"
            output_file = input("\n💾 Nombre del archivo de salida [transcription.txt]: ").strip() or "transcription.txt"
            
            print("\n🔄 Descargando y procesando el video...\n")
            main(youtube_url, is_youtube=True, model=model, output_file=output_file)

        elif opcion == "0":
            print("\n👋 Saliendo del programa...")
            exit()
        else:
            print("\n❌ Opción inválida, intenta de nuevo.")
