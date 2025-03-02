class TranscriptionSaver:
    @staticmethod
    def guardar_transcripcion(texto: str, archivo_salida: str):
        with open(archivo_salida, "w", encoding="utf-8") as f:
            f.write(texto)
