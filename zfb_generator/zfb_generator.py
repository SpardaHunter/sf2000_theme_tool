import tkinter as tk
from zfb_generator.ZFBimagesTool import ZFBimagesTool
from zfb_generator.ZFBimagesToolSpardaARCADE import ZFBApplicationArcade

class ZFBGenerator(tk.Frame):
    def __init__(self, root):
        super().__init__(root)

        # Etiqueta de título
        self.label = tk.Label(self, text="ZFB Generator")
        self.label.pack(pady=20)

        # Botón para mostrar la clase ZFB Generator
        btn_12 = tk.Button(self, text="ZFB Generator", command=lambda: self.show_frogtool('x'), width=25, height=2)
        btn_12.pack(pady=10)

        # Botón para mostrar la clase ZFB Generator Arcade
        btn_7 = tk.Button(self, text="ZFB Generator Arcade", command=lambda: self.show_frogtool('e'), width=25, height=2)
        btn_7.pack(pady=10)

    def show_frogtool(self, version):
        """Mostrar la interfaz correspondiente (FrogtoolGUIx o FrogtoolGUIe) dependiendo del parámetro."""
        if version == 'x':
            # Cambiar a ZFB Generator
            self.master.change_frame(ZFBimagesTool(self.master))
        elif version == 'e':
            # Cambiar a ZFB Generator Arcade
            self.master.change_frame(ZFBApplicationArcade(self.master))
