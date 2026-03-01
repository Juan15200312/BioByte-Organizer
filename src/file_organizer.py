import os

from cryptography.fernet import Fernet
class FileOrganizer:
    def __init__(self):
        self.carpeta = ""
        self.rules = {
            ".pdf": "Documentos",
            ".docx": "Documentos",
            ".img": "Imágenes",
            ".png": "Imágenes",
            ".jpg": "Imágenes",
            ".mp4": "Videos",
            ".avi": "Videos",
            ".mkv": "Videos",
            ".webm": "Videos",
            ".mp3": "Música",
            ".acc": "Música",
            ".ogg": "Música",
            ".wav": "Música",
        }
        self.respaldo_activado = False
        self.encriptado_activado = False
        self.orden = "carpeta"

        self.key = None
        self.cifrar = None

    def set_ruta_base(self, path):
        self.carpeta = path

    def activar_respaldo(self, value: bool):
        self.respaldo_activado = value

    def activar_encriptado(self, value: bool):
        self.encriptado_activado = value
        if value:
            self.key = Fernet.generate_key()
            self.cifrar = Fernet(self.key)

    def escanear_archivos(self):
        if not self.carpeta:
            return []

        archivos_validos = []

        archivos = os.listdir(self.carpeta)

        for archivo in archivos:
            ruta_entera = os.path.join(self.carpeta, archivo)

            if os.path.isfile(ruta_entera):
                archivos_validos.append(archivo)

        if self.orden == "tamanio":
            archivos_validos.sort(key=lambda a: os.path.getsize(os.path.join(self.carpeta, a)), reverse=False)
        elif self.orden == "fecha":
            archivos_validos.sort(key=lambda a: os.path.getmtime(os.path.join(self.carpeta, a)), )

        else:
            archivos_validos.sort()
        return archivos_validos


