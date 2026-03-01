import os
import shutil
from datetime import datetime


def destinacion_ficheros(self, filename):
    extension = os.path.splitext(filename)[1]
    extension = extension.lower()
    return self.rules.get(extension, "Otros")


def copia_Seguridad(self, filepath):
    backup_path = os.path.join(self.base_path, "Backup")
    os.makedirs(backup_path, exist_ok=True)
    shutil.copy(filepath, backup_path)


def encriptacion(self, filepath):
    with open(filepath, "rb") as f:
        data = f.read()
    contenido_cifrado = self.cipher.encrypt(data)
    with open(filepath, "wb") as f:
        f.write(contenido_cifrado)


def proceso(self, filename):
    origen = os.path.join(self.base_path, filename)
    carpeta_destino = self.get_destination_folder(filename)
    ruta_destino = os.path.join(self.base_path, carpeta_destino)

    os.makedirs(carpeta_destino, exist_ok=True)
    destino = os.path.join(carpeta_destino, filename)

    try:
        if self.backup_enabled:
            self.backup_file(origen)

        if self.encrypt_enabled:
            self.encrypt_file(origen)

        shutil.move(origen, destino)

        return {
            "archivo": filename,
            "destino": carpeta_destino,
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "estado": "OK"
        }

    except Exception as error:
        return {
            "archivo": filename,
            "destino": "-",
            "fecha": datetime.now().strftime("%Y-%m-%d %H:%M"),
            "estado": f"ERROR: {error}"
        }

#La Ejecución

def run(self):
    results = []
    for archivo in self.scan_files():
        results.append(self.process_file(archivo))
    return results