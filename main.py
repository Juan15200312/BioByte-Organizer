import platform

def verificar_os():
    if platform.system() == "Linux":
        print("Ejecutando BioByte Organizer en Linux")
        return True
    print("Ejecutando BioByte Organizer en Windows")
    return False


def main():

    try:
        print("Iniciando organización...")


        print("Proceso finalizado!")
    except FileNotFoundError:
        print("Error: ")

