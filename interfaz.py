import tkinter as tk
from tkinter import messagebox, filedialog
import customtkinter as ctk
from PIL import Image
from file_organizer import FileOrganizer # ← CONEXIÓN REAL


colores = {
    'verde': '#31C204',
    'rojo': '#C21704',
    'bg_prin': '#FFF9F7',
    'bg_cont': '#CFCDCC',
    'bg_ter': 'white'
}


def centrar_ventana(ventana, ancho, alto):
    pantalla_ancho = ventana.winfo_screenwidth()
    pantalla_alto = ventana.winfo_screenheight()

    x = int((pantalla_ancho / 2) - (ancho / 2))
    y = int((pantalla_alto / 2) - (alto / 2))
    return ventana.geometry(f"{ancho}x{alto}+{x}+{y}")


class App(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master, bg=colores['bg_prin'])
        self.pack(fill="both", expand=True)

        self.organizer = FileOrganizer()

        # VARIABLES
        self.ruta_var = ctk.StringVar(value='Seleccione una carpeta...')
        self.switch_var = ctk.StringVar(value="off")
        self.copia_seg_var = ctk.BooleanVar(value=False)
        self.encriptar_var = ctk.BooleanVar(value=False)

        self.ord_fecha_var = ctk.BooleanVar(value=False)
        self.ord_carpeta_var = ctk.BooleanVar(value=True)
        self.ord_tamano_var = ctk.BooleanVar(value=False)

        self.crear_widgets()

    # ACTUALIZAR RESUMEN

    def actualizar_resumen(self, cantidad, hizo_copia):

        self.archMovidosResumen.configure(text=f"Archivos movidos ➡ {cantidad}")

        txt_copia = "Sí (Encriptada)" if self.encriptar_var.get() else "Sí"
        self.copiaSegResumen.configure(
            text=f"Copia de Seguridad ➡ {txt_copia if hizo_copia else 'No'}"
        )

        criterio = "Carpeta"
        if self.ord_fecha_var.get(): criterio = "Fecha"
        if self.ord_tamano_var.get(): criterio = "Tamaño"

        self.organizadoPorResumen.configure(text=f"Organizado por ➡ {criterio}")

        self.encriptadoSegResumen.configure(
            text=f"Encriptado ➡ {'Sí' if self.encriptar_var.get() else 'No'}"
        )

    # APLICAR CRITERIO DE ORDEN

    def aplicar_criterio_orden(self):
        if self.ord_fecha_var.get():
            self.organizer.set_sorting("fecha")
        elif self.ord_tamano_var.get():
            self.organizer.set_sorting("tamano")
        else:
            self.organizer.set_sorting("carpeta")

    # CREAR WIDGETS

    def crear_widgets(self):

        # PRIMER DIV
        self.contenedor1 = ctk.CTkFrame(
            self, bg_color=colores['bg_prin'], fg_color=colores['bg_cont'],
            border_width=1, border_color=colores['bg_cont'], corner_radius=10
        )
        self.contenedor1.pack(pady=20, padx=20, fill='x')
        self.contenedor1.grid_columnconfigure(1, weight=1)

        self.punto = ctk.CTkFrame(
            self.contenedor1, bg_color=colores['bg_cont'], fg_color=colores['rojo'],
            border_width=2, border_color='black', corner_radius=10, height=15, width=15
        )
        self.punto.grid(row=0, column=0, padx=(20, 0), pady=10, sticky='w')

        self.etiqueta = ctk.CTkLabel(
            self.contenedor1, text="Listo para empezar",
            text_color='black', font=('Arial', 14, 'bold')
        )
        self.etiqueta.grid(row=0, column=1, padx=(10, 0), pady=10, sticky="w")

        def switch_event():

            nuevo_texto = "Apagar" if self.switch_var.get() == "on" else "Encender"
            self.switch.configure(text=nuevo_texto)

            nuevo_color = colores['verde'] if self.switch_var.get() == "on" else colores['rojo']
            self.punto.configure(fg_color=nuevo_color)

            etiqueta_estado = 'Escaneando...' if self.switch_var.get() == 'on' else 'Listo para empezar'
            self.etiqueta.configure(text=etiqueta_estado)

            if self.switch_var.get() == "on":

                # Bloquear controles
                self.select_folder.configure(state='disabled')
                self.checkCopiaSeguridad.configure(state='disabled')
                self.checkEncriptar.configure(state='disabled')
                self.checkOrdTamano.configure(state='disabled')
                self.checkOrdFecha.configure(state='disabled')
                self.checkOrdCarpeta.configure(state='disabled')

                # Aplicar configuración
                self.aplicar_criterio_orden()
                self.organizer.enable_backup(self.copia_seg_var.get())
                self.organizer.enable_encryption(self.encriptar_var.get())

                # Ejecutar organizador
                resultados = self.organizer.run()

                cantidad = len(resultados)
                hizo_copia = self.copia_seg_var.get()

                self.actualizar_resumen(cantidad, hizo_copia)

            else:
                # Desbloquear controles
                self.select_folder.configure(state='normal')
                self.checkCopiaSeguridad.configure(state='normal')
                self.checkEncriptar.configure(state='normal')
                self.checkOrdTamano.configure(state='normal')
                self.checkOrdFecha.configure(state='normal')
                self.checkOrdCarpeta.configure(state='normal')

        # SWITCH
        self.switch = ctk.CTkSwitch(
            self.contenedor1, text="Encender", text_color='black',
            font=('Arial', 14, 'bold'), command=switch_event,
            variable=self.switch_var, onvalue="on", offvalue="off",
            progress_color=colores['verde'], state='disabled'
        )
        self.switch.grid(row=0, column=1, padx=20, pady=10, sticky='e')

        # SEGUNDO DIV (SELECCIÓN DE CARPETA)

        self.contenedor2 = ctk.CTkFrame(
            self, bg_color=colores['bg_prin'], fg_color=colores['bg_cont'],
            border_width=1, border_color=colores['bg_cont'], corner_radius=10
        )
        self.contenedor2.pack(pady=0, padx=20, fill='x')
        self.contenedor2.grid_columnconfigure(1, weight=1)

        self.iconFolder = ctk.CTkImage(
            light_image=Image.open('./images/folder.png'), size=(25, 25)
        )
        self.icon_label = ctk.CTkLabel(self.contenedor2, image=self.iconFolder, text="")
        self.icon_label.grid(row=0, column=0, padx=(20, 0), pady=10, sticky='w')

        def select_folder():
            carpeta = filedialog.askdirectory(title="Seleccionar Carpeta")
            if carpeta:
                self.ruta_var.set(carpeta)
                self.organizer.set_base_path(carpeta)
                self.switch.configure(state='normal')
                messagebox.showinfo("Seleccionar carpeta", f"Se seleccionó la carpeta:\n{carpeta}")

        self.rutaLabel = ctk.CTkLabel(
            self.contenedor2, textvariable=self.ruta_var,
            text_color='gray', font=('Arial', 14, 'bold')
        )
        self.rutaLabel.grid(row=0, column=1, padx=20, pady=10, sticky='w')

        self.select_folder = ctk.CTkButton(
            self.contenedor2, text='Cambiar', fg_color=colores['verde'],
            font=('Arial', 14, 'bold'), text_color='white',
            command=select_folder, hover_color='black'
        )
        self.select_folder.grid(row=0, column=2, padx=20, pady=10, sticky='e')

        # TERCER DIV (REGLAS + OPCIONES)

        self.contenedor3 = ctk.CTkFrame(
            self, bg_color=colores['bg_prin'], fg_color=colores['bg_cont'],
            border_width=1, border_color=colores['bg_cont'], corner_radius=10
        )
        self.contenedor3.pack(pady=20, padx=20, fill='x')
        self.contenedor3.grid_columnconfigure(0, weight=3)
        self.contenedor3.grid_columnconfigure(1, weight=7)

        # REGLAS

        self.contenedor31 = ctk.CTkFrame(
            self.contenedor3, bg_color=colores['bg_cont'], fg_color=colores['bg_ter'],
            border_width=1, border_color=colores['bg_ter'], corner_radius=10
        )
        self.contenedor31.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.label_Reglas = ctk.CTkLabel(
            self.contenedor31, text='Reglas de extensión:',
            text_color='black', font=('Arial', 14, 'bold')
        )
        self.label_Reglas.grid(row=0, column=0, padx=10, pady=10)

        reglas = [
            ".pdf .docx  ➡  /Documentos",
            ".img .png .jpg  ➡  /Imágenes",
            ".mp4 .avi .mkv .webm  ➡  /Videos",
            ".mp3 .acc .ogg .wav  ➡  /Música",
            ".xyz .abc .jaja .jeje  ➡  /Otros"
        ]

        for i, texto in enumerate(reglas, start=1):
            ctk.CTkLabel(
                self.contenedor31, text=texto, text_color='black', font=('Arial', 12)
            ).grid(row=i, column=0, padx=10, pady=2)

        # OPCIONES

        self.contenedor32 = ctk.CTkFrame(
            self.contenedor3, bg_color=colores['bg_cont'], fg_color=colores['bg_cont'],
            border_width=1, border_color=colores['bg_cont'], corner_radius=10
        )
        self.contenedor32.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')

        # COPIA Y ENCRIPTACIÓN
        self.contenedor321 = ctk.CTkFrame(
            self.contenedor32, bg_color=colores['bg_cont'], fg_color=colores['bg_ter'],
            border_width=1, border_color=colores['bg_ter'], corner_radius=10
        )
        self.contenedor321.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')

        self.checkCopiaSeguridad = ctk.CTkCheckBox(
            self.contenedor321, text='Realizar una copia de seguridad',
            text_color='black', fg_color=colores['verde'],
            variable=self.copia_seg_var
        )
        self.checkCopiaSeguridad.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        self.checkEncriptar = ctk.CTkCheckBox(
            self.contenedor321, text='Encriptar copia de seguridad',
            text_color='black', fg_color=colores['verde'],
            variable=self.encriptar_var
        )
        self.checkEncriptar.grid(row=0, column=1, padx=10, pady=5, sticky='e')

        # ORDENACIÓN
        self.contenedor322 = ctk.CTkFrame(
            self.contenedor32, bg_color=colores['bg_cont'], fg_color=colores['bg_ter'],
            border_width=1, border_color=colores['bg_ter'], corner_radius=10
        )
        self.contenedor322.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')

        self.labelOrd = ctk.CTkLabel(
            self.contenedor322, text='Ordenar por:',
            text_color='black', font=('Arial', 12, 'bold')
        )
        self.labelOrd.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        self.checkOrdFecha = ctk.CTkCheckBox(
            self.contenedor322, text='Fecha', text_color='black',
            fg_color=colores['verde'], variable=self.ord_fecha_var
        )
        self.checkOrdFecha.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        self.checkOrdCarpeta = ctk.CTkCheckBox(
            self.contenedor322, text='Carpeta', text_color='black',
            fg_color=colores['verde'], variable=self.ord_carpeta_var
        )
        self.checkOrdCarpeta.grid(row=0, column=2, padx=10, pady=5, sticky='w')

        self.checkOrdTamano = ctk.CTkCheckBox(
            self.contenedor322, text='Tamaño', text_color='black',
            fg_color=colores['verde'], variable=self.ord_tamano_var
        )
        self.checkOrdTamano.grid(row=0, column=3, padx=10, pady=5, sticky='w')

        # RESUMEN FINAL
        self.contenedor4 = ctk.CTkFrame(
            self, bg_color=colores['bg_prin'], fg_color=colores['bg_cont'],
            border_width=1, border_color=colores['bg_cont'], corner_radius=10
        )
        self.contenedor4.pack(pady=(0, 20), padx=20, fill='x')

        self.tituloResumen = ctk.CTkLabel(
            self.contenedor4, text='Resumen de la operación:',
            text_color='black', font=('Arial', 14, 'bold')
        )
        self.tituloResumen.grid(row=0, column=0, padx=10, pady=5)

        self.contenedorDatos = ctk.CTkFrame(
            self.contenedor4, bg_color=colores['bg_cont'], fg_color=colores['bg_ter'],
            border_width=1, border_color=colores['bg_ter'], corner_radius=10
        )
        self.contenedorDatos.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')

        self.archMovidosResumen = ctk.CTkLabel(
            self.contenedorDatos, text='Archivos movidos ➡ 0',
            text_color='black', font=('Arial', 14, 'bold')
        )
        self.archMovidosResumen.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        self.copiaSegResumen = ctk.CTkLabel(
            self.contenedorDatos, text='Copia de Seguridad ➡ No',
            text_color='black', font=('Arial', 14, 'bold')
        )
        self.copiaSegResumen.grid(row=2, column=0, padx=10, pady=5, sticky='w')

        self.encriptadoSegResumen = ctk.CTkLabel(
            self.contenedorDatos, text='Encriptado ➡ No',
            text_color='black', font=('Arial', 14, 'bold')
        )
        self.encriptadoSegResumen.grid(row=3, column=0, padx=10, pady=5, sticky='w')

        self.organizadoPorResumen = ctk.CTkLabel(
            self.contenedorDatos, text='Organizado por ➡ Carpeta',
            text_color='black', font=('Arial', 14, 'bold')
        )
        self.organizadoPorResumen.grid(row=4, column=0, padx=10, pady=5, sticky='w')
