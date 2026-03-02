import os
import shutil
from datetime import datetime
from cryptography.fernet import Fernet


class FileOrganizer:
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
        self.backup_enabled = False
        self.encrypt_enabled = False
        self.sort_by = "carpeta"

        self.key = None
        self.cipher = None

    # CONFIGURACIÓN

    def set_base_path(self, path):
        self.base_path = path

    def enable_backup(self, value: bool):
        self.backup_enabled = value

    def enable_encryption(self, value: bool):
        self.encrypt_enabled = value
        if value:
            self.key = Fernet.generate_key()
            self.cipher = Fernet(self.key)

    def set_sorting(self, mode):
        self.sort_by = mode

    # ESCANEO Y ORDENACIÓN

    def scan_files(self):
        if not self.base_path:
            return []

        files = [
            f for f in os.listdir(self.base_path)
            if os.path.isfile(os.path.join(self.base_path, f))
        ]

        if self.sort_by == "fecha":
            files.sort(
                key=lambda f: os.path.getmtime(os.path.join(self.base_path, f)),
                reverse=False
            )

        elif self.sort_by == "tamano":
            files.sort(
                key=lambda f: os.path.getsize(os.path.join(self.base_path, f))
            )

        else:
            files.sort()

        return files

    # PROCESADO

    def get_destination_folder(self, filename):
        ext = os.path.splitext(filename)[1].lower()
        return self.rules.get(ext, "Otros")

    def backup_file(self, filepath):
        backup_dir = os.path.join(self.base_path, "Backup")
        os.makedirs(backup_dir, exist_ok=True)
        shutil.copy(filepath, backup_dir)

    def encrypt_file(self, filepath):
        with open(filepath, "rb") as f:
            data = f.read()
        encrypted = self.cipher.encrypt(data)
        with open(filepath, "wb") as f:
            f.write(encrypted)

    def process_file(self, filename):
        src = os.path.join(self.base_path, filename)
        dest_folder = os.path.join(self.base_path, self.get_destination_folder(filename))
        os.makedirs(dest_folder, exist_ok=True)
        dest = os.path.join(dest_folder, filename)

        try:
            if self.backup_enabled:
                self.backup_file(src)

            if self.encrypt_enabled:
                self.encrypt_file(src)

            shutil.move(src, dest)

            return {
                "archivo": filename,
                "destino": dest_folder,
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "estado": "OK"
            }

        except Exception as e:
            return {
                "archivo": filename,
                "destino": "-",
                "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
                "estado": f"ERROR: {str(e)}"
            }

    def run(self):
        results = []
        for f in self.scan_files():
            results.append(self.process_file(f))
        return results
