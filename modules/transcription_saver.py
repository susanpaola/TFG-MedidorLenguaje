def save_transcription(text, file_path):
    with open(file_path, "w", encoding="utf-8") as file:
        file.write(text)
