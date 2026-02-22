import platform
import tkinter as tk
from interfaz import App, centrar_ventana


def verificar_os():
    if platform.system() == "Linux":
        print("Ejecutando BioByte Organizer en Linux")
        return True
    print("Ejecutando BioByte Organizer en Windows")
    return False


def main():
    try:
        print("Iniciando organización...")
        root = tk.Tk()
        root.title("BioByte Organizer")
        imagen = tk.PhotoImage(file="./images/folder2.png")
        root.wm_iconphoto(False, imagen)

        centrar_ventana(root, 800, 620)

        app = App(master=root)
        app.mainloop()

        print("Proceso finalizado!")
    except FileNotFoundError:
        print("Error: ")



if __name__ == "__main__":
    main()