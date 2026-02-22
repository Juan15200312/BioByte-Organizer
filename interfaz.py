import tkinter as tk
from tkinter import messagebox, filedialog
import customtkinter as ctk
from PIL import Image

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

        self.ruta_var = ctk.StringVar(value='Seleccione una carpeta...')
        self.switch_var = ctk.StringVar(value="off")
        self.copia_seg_var = ctk.BooleanVar(value=False)
        self.encriptar_var = ctk.BooleanVar(value=False)

        self.ord_fecha_var = ctk.BooleanVar(value=False)
        self.ord_carpeta_var = ctk.BooleanVar(value=True)
        self.ord_tamano_var = ctk.BooleanVar(value=False)

        self.crear_widgets()

    def actualizar_resumen(self, cantidad, hizo_copia):
        # 1. Actualizar cantidad
        self.res_archivos.configure(text=f"{cantidad} archivos")

        # 2. Actualizar texto de copia
        txt_copia = "Realizada (Encriptada)" if self.encriptar_var.get() else "Realizada"
        self.res_copia.configure(text=txt_copia if hizo_copia else "No realizada")

        # 3. Mostrar criterio de orden (basado en tus checkboxes)
        criterio = "Carpeta"
        if self.ord_fecha_var.get(): criterio = "Fecha"
        if self.ord_tamano_var.get(): criterio = "Tamaño"
        self.res_criterio.configure(text=criterio)

        # 4. Mensaje final
        self.res_estado_final.configure(text="¡Operación completada con éxito!", text_color=colores['verde'])

    def crear_widgets(self):
        # PRIMER DIV
        self.contenedor1 = ctk.CTkFrame(self, bg_color=colores['bg_prin'], fg_color=colores['bg_cont'],
                                        border_width=1, border_color=colores['bg_cont'], corner_radius=10, height=50
                                        )
        self.contenedor1.pack(pady=20, padx=20, fill='x')
        self.contenedor1.grid_columnconfigure(1, weight=1)

        self.punto = ctk.CTkFrame(self.contenedor1, bg_color=colores['bg_cont'], fg_color=colores['rojo'],
                                  border_width=2, border_color='black', corner_radius=10, height=15, width=15
                                  )
        self.punto.grid(row=0, column=0, padx=(20, 0), pady=10, sticky='w')

        self.etiqueta = ctk.CTkLabel(self.contenedor1, text="Listo para empezar",
                                     text_color='black', font=('Arial', 14, 'bold'),
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
                self.select_folder.configure(state='disabled')
                self.checkCopiaSeguridad.configure(state='disabled')
                self.checkEncriptar.configure(state='disabled')
                self.checkOrdTamano.configure(state='disabled')
                self.checkOrdFecha.configure(state='disabled')
                self.checkOrdCarpeta.configure(state='disabled')
            else:
                self.select_folder.configure(state='normal')
                self.checkCopiaSeguridad.configure(state='normal')
                self.checkEncriptar.configure(state='normal')
                self.checkOrdTamano.configure(state='normal')
                self.checkOrdFecha.configure(state='normal')
                self.checkOrdCarpeta.configure(state='normal')

            print(f"Estado: {self.switch_var.get()}")

        self.switch = ctk.CTkSwitch(
            self.contenedor1,
            text="Encender",
            text_color='black',
            font=('Arial', 14, 'bold'),
            command=switch_event,
            variable=self.switch_var,
            onvalue="on",
            offvalue="off",
            progress_color=colores['verde'],
            state='disabled',
        )
        self.switch.grid(row=0, column=1, padx=20, pady=10, sticky='e')

        # SEGUNDO DIV
        self.contenedor2 = ctk.CTkFrame(self, bg_color=colores['bg_prin'], fg_color=colores['bg_cont'],
                                        border_width=1, border_color=colores['bg_cont'], corner_radius=10, height=50
                                        )
        self.contenedor2.pack(pady=0, padx=20, fill='x')
        self.contenedor2.grid_columnconfigure(1, weight=1)

        self.iconFolder = ctk.CTkImage(
            light_image=Image.open('./images/folder.png'), size=(25, 25),
        )
        self.icon_label = ctk.CTkLabel(self.contenedor2, image=self.iconFolder, text="")
        self.icon_label.grid(row=0, column=0, padx=(20, 0), pady=10, sticky='w')

        def select_folder():
            carpeta = filedialog.askdirectory(title="Seleccionar Carpeta")
            if carpeta:
                self.ruta_var.set(carpeta)
                self.switch.configure(state='normal')
                messagebox.showinfo(title='Seleccionar carpeta', message=f'Se selecciono la carpeta: {carpeta}')

        self.rutaLabel = ctk.CTkLabel(self.contenedor2, textvariable=self.ruta_var,
                                      text_color='gray', font=('Arial', 14, 'bold'),
                                      )
        self.rutaLabel.grid(row=0, column=1, padx=20, pady=10, sticky='w')

        self.select_folder = ctk.CTkButton(
            self.contenedor2,
            text='Cambiar',
            fg_color=colores['verde'],
            font=('Arial', 14, 'bold'),
            text_color='white',
            command=select_folder,
            state='normal',
            hover_color='black',
            text_color_disabled='gray',
        )
        self.select_folder.grid(row=0, column=2, padx=20, pady=10, sticky='e')

        # TERCER DIV
        self.contenedor3 = ctk.CTkFrame(self, bg_color=colores['bg_prin'], fg_color=colores['bg_cont'],
                                        border_width=1, border_color=colores['bg_cont'], corner_radius=10, height=50
                                        )
        self.contenedor3.pack(pady=20, padx=20, fill='x')
        self.contenedor3.grid_columnconfigure(0, weight=3)
        self.contenedor3.grid_columnconfigure(1, weight=7)

        # DIV DE REGLAS
        self.contenedor31 = ctk.CTkFrame(self.contenedor3, bg_color=colores['bg_cont'], fg_color=colores['bg_ter'],
                                         border_width=1, border_color=colores['bg_ter'], corner_radius=10, height=50
                                         )

        self.contenedor31.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')
        self.contenedor31.grid_columnconfigure(0, weight=1)
        self.contenedor31.grid_rowconfigure(0, weight=1)

        self.label_Reglas = ctk.CTkLabel(self.contenedor31, text='Reglas de extension:', text_color='black',
                                         font=('Arial', 14, 'bold'), anchor='center')
        self.label_Reglas.grid(row=0, column=0, padx=10, pady=10, sticky='nsew')

        self.label_Reglas_Doc = ctk.CTkLabel(self.contenedor31, text='.pdf .docx  ➡  /Documentos', text_color='black',
                                             font=('Arial', 12), anchor='center')
        self.label_Reglas_Doc.grid(row=1, column=0, padx=10, pady=0, sticky='nsew')
        self.label_Reglas_Img = ctk.CTkLabel(self.contenedor31, text='.img .png .jpg  ➡  /Imágenes',
                                             text_color='black',
                                             font=('Arial', 12), anchor='center')
        self.label_Reglas_Img.grid(row=2, column=0, padx=10, pady=0, sticky='nsew')

        self.label_Reglas_Vid = ctk.CTkLabel(self.contenedor31, text='.mp4 .avi .mkv .webm  ➡  /Videos',
                                             text_color='black',
                                             font=('Arial', 12), anchor='center')
        self.label_Reglas_Vid.grid(row=3, column=0, padx=10, pady=0, sticky='nsew')

        self.label_Reglas_Mus = ctk.CTkLabel(self.contenedor31, text='.mp3 .acc .ogg .wav  ➡  /Musica',
                                             text_color='black',
                                             font=('Arial', 12), anchor='center')
        self.label_Reglas_Mus.grid(row=4, column=0, padx=10, pady=0, sticky='nsew')

        self.label_Reglas_Otr = ctk.CTkLabel(self.contenedor31, text='.xyz .abc .jaja .jeje  ➡  /Otros',
                                             text_color='black',
                                             font=('Arial', 12), anchor='center')
        self.label_Reglas_Otr.grid(row=5, column=0, padx=10, pady=0, sticky='nsew')

        # DIV DE OPCIONES
        self.contenedor32 = ctk.CTkFrame(self.contenedor3, bg_color=colores['bg_cont'], fg_color=colores['bg_cont'],
                                         border_width=1, border_color=colores['bg_cont'], corner_radius=10, height=50
                                         )

        self.contenedor32.grid(row=0, column=1, padx=5, pady=5, sticky='nsew')
        self.contenedor32.grid_rowconfigure(0, weight=5)
        self.contenedor32.grid_columnconfigure(0, weight=10)
        self.contenedor32.grid_rowconfigure(1, weight=5)

        self.contenedor321 = ctk.CTkFrame(self.contenedor32, bg_color=colores['bg_cont'], fg_color=colores['bg_ter'],
                                          border_width=1, border_color=colores['bg_ter'], corner_radius=10, height=50
                                          )
        self.contenedor321.grid(row=0, column=0, padx=5, pady=5, sticky='nsew')
        self.contenedor321.grid_columnconfigure(0, weight=1)
        self.contenedor321.grid_columnconfigure(1, weight=1)
        self.contenedor321.grid_rowconfigure(0, weight=1)

        self.checkCopiaSeguridad = ctk.CTkCheckBox(self.contenedor321, text='Realizar una copia de seguridad',
                                                   text_color='black', hover_color=colores['verde'],
                                                   checkmark_color='white',
                                                   fg_color=colores['verde'],
                                                   variable=self.copia_seg_var
                                                   )
        self.checkCopiaSeguridad.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        self.checkEncriptar = ctk.CTkCheckBox(self.contenedor321, text='Encriptar copia de seguridad',
                                              text_color='black', hover_color=colores['verde'],
                                              checkmark_color='white',
                                              fg_color=colores['verde'],
                                              variable=self.encriptar_var
                                              )
        self.checkEncriptar.grid(row=0, column=1, padx=10, pady=5, sticky='e')

        self.contenedor322 = ctk.CTkFrame(self.contenedor32, bg_color=colores['bg_cont'], fg_color=colores['bg_ter'],
                                          border_width=1, border_color=colores['bg_ter'], corner_radius=10, height=50
                                          )
        self.contenedor322.grid(row=1, column=0, padx=5, pady=5, sticky='nsew')
        self.contenedor322.grid_columnconfigure(0, weight=4)
        self.contenedor322.grid_columnconfigure(1, weight=2)
        self.contenedor322.grid_columnconfigure(2, weight=2)
        self.contenedor322.grid_columnconfigure(3, weight=2)
        self.contenedor322.grid_rowconfigure(0, weight=1)

        self.labelOrd = ctk.CTkLabel(self.contenedor322, text='Ordenar por:',
                                     text_color='black',
                                     font=('Arial', 12, 'bold'), anchor='center', )
        self.labelOrd.grid(row=0, column=0, padx=10, pady=5, sticky='w')

        self.checkOrdFecha = ctk.CTkCheckBox(self.contenedor322, text='Fecha',
                                             text_color='black', hover_color=colores['verde'],
                                             checkmark_color='white',
                                             fg_color=colores['verde'],
                                             variable=self.ord_fecha_var
                                             )
        self.checkOrdFecha.grid(row=0, column=1, padx=10, pady=5, sticky='w')

        self.checkOrdCarpeta = ctk.CTkCheckBox(self.contenedor322, text='Carpeta',
                                               text_color='black', hover_color=colores['verde'],
                                               checkmark_color='white',
                                               fg_color=colores['verde'],
                                               variable=self.ord_carpeta_var
                                               )
        self.checkOrdCarpeta.grid(row=0, column=2, padx=10, pady=5, sticky='w')

        self.checkOrdTamano = ctk.CTkCheckBox(self.contenedor322, text='Carpeta',
                                              text_color='black', hover_color=colores['verde'],
                                              checkmark_color='white',
                                              fg_color=colores['verde'],
                                              variable=self.ord_tamano_var
                                              )
        self.checkOrdTamano.grid(row=0, column=3, padx=10, pady=5, sticky='w')

        # ULTIMO DIV
        self.contenedor4 = ctk.CTkFrame(self, bg_color=colores['bg_prin'], fg_color=colores['bg_cont'],
                                        border_width=1, border_color=colores['bg_cont'], corner_radius=10, height=50
                                        )
        self.contenedor4.pack(pady=(0,20), padx=20, fill='x')
        self.contenedor4.columnconfigure(0, weight=1)
        self.contenedor4.rowconfigure(0, weight=1)

        self.tituloResumen = ctk.CTkLabel(self.contenedor4, text='Resumen de la operacion: ', text_color='black',
                                          font=('Arial', 14, 'bold'), anchor='center',
                                          )
        self.tituloResumen.grid(row=0, column=0, padx=10, pady=5, sticky='nsew')

        self.contenedorDatos = ctk.CTkFrame(self.contenedor4, bg_color=colores['bg_cont'], fg_color=colores['bg_ter'],
                                         border_width=1, border_color=colores['bg_ter'], corner_radius=10, height=50
                                         )

        self.contenedorDatos.grid(row=1, column=0, padx=10, pady=10, sticky='nsew')
        self.contenedorDatos.grid_columnconfigure(0, weight=1)
        self.contenedorDatos.grid_rowconfigure(0, weight=1)

        self.archMovidosResumen = ctk.CTkLabel(self.contenedorDatos, text=f'Archivos movidos  ➡  0', text_color='black',
                                               font=('Arial', 14, 'bold')
                                               )
        self.archMovidosResumen.grid(row=1, column=0, padx=10, pady=5, sticky='w')

        self.copiaSegResumen = ctk.CTkLabel(self.contenedorDatos, text=f'Copia de Seguridad  ➡  Si', text_color='black',
                                            font=('Arial', 14, 'bold')
                                            )
        self.copiaSegResumen.grid(row=2, column=0, padx=10, pady=5, sticky='w')

        self.encriptadoSegResumen = ctk.CTkLabel(self.contenedorDatos, text=f'Encriptado  ➡  No', text_color='black',
                                                 font=('Arial', 14, 'bold')
                                                 )
        self.encriptadoSegResumen.grid(row=3, column=0, padx=10, pady=5, sticky='w')

        self.organizadoPorResumen = ctk.CTkLabel(self.contenedorDatos, text=f'Organizado por  ➡  Fecha', text_color='black',
                                                 font=('Arial', 14, 'bold')
                                                 )
        self.organizadoPorResumen.grid(row=4, column=0, padx=10, pady=5, sticky='w')