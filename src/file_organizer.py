import os
import shutil
from datetime import datetime
from cryptography.fernet import Fernet



class OrganizarArchivos:
    def __init__(self):
        self.base_path = ""
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
        self.ordenar_por = "carpeta"

        self.key = None
        self.cifrar = None


    def set_ruta_base(self, path):
        self.base_path = path

    def activar_respaldo(self, value: bool):
        self.respaldo_activado = value

    def activar_encriptado(self, value: bool):
        self.encriptado_activado = value
        if value:
            self.key = Fernet.generate_key()
            self.cifrar = Fernet(self.key)

    def set_ordenar(self, mode):
        self.ordenar_por = mode

    def escanear_archivos(self):
        if not self.base_path:
            return []

        files = [
            f for f in os.listdir(self.base_path)
            if os.path.isfile(os.path.join(self.base_path, f))
        ]

        if self.ordenar_por == "fecha":
            files.sort(
                key=lambda f: os.path.getmtime(os.path.join(self.base_path, f)),
                reverse=False
            )

        elif self.ordenar_por == "tamano":
            files.sort(
                key=lambda f: os.path.getsize(os.path.join(self.base_path, f))
            )

        else:
            files.sort()

        return files

    def get_carpeta_destino(self, nombre_archivo):
        ext = os.path.splitext(nombre_archivo)[1].lower()
        return self.rules.get(ext, "Otros")

    def respaldar_archivo(self, ruta_archivo):
        carpeta_respaldo= os.path.join(self.base_path, "Backup")
        os.makedirs(carpeta_respaldo, exist_ok=True)
        shutil.copy(ruta_archivo, carpeta_respaldo)

    def encriptar_archivo(self, ruta_archivo):
        with open(ruta_archivo, "rb") as f:
            data = f.read()
        datos_encriptados = self.cifrar.encrypt(data)
        with open(ruta_archivo, "wb") as f:
            f.write(datos_encriptados)

    def procesar_archivo(self, nombre_archivo):
        origen = os.path.join(self.base_path, nombre_archivo)
        carpeta_destino = os.path.join(self.base_path, self.get_carpeta_destino(nombre_archivo))
        os.makedirs(carpeta_destino, exist_ok=True)
        dest = os.path.join(carpeta_destino, nombre_archivo)

        try:
            if self.respaldo_activado:
                self.respaldar_archivo(origen)

            if self.encriptado_activado:
                self.encriptar_archivo(origen)

            shutil.move(origen, dest)

            return {
                "archivo": nombre_archivo,
                "destino": carpeta_destino,
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "estado": "OK"
            }

        except Exception as e:
            return {
                "archivo": nombre_archivo,
                "destino": "-",
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "estado": f"ERROR: {str(e)}"
            }

    def run(self):
        resultados = []
        for f in self.escanear_archivos():
            resultados.append(self.procesar_archivo(f))
        return resultados


