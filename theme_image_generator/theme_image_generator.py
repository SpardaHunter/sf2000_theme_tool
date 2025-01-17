import tkinter as tk
#from theme_image_generator.Theme_Editor import ImageProcessorApp
#from theme_image_generator.Theme_Editor_SOP import ImageProcessorAppSOP

class ThemeGenerator(tk.Frame):
    def __init__(self, root):
        super().__init__(root)

        # Etiqueta de título
        self.label = tk.Label(self, text="Theme Generator")
        self.label.pack(pady=20)

        # Botón para mostrar la clase Theme Editor SOP
        btn_12 = tk.Button(self, text="Theme Editor SOP", command=lambda: self.show_frogtool('x'), width=25, height=2)
        btn_12.pack(pady=10)

        # Botón para mostrar la clase Theme Editor
        btn_7 = tk.Button(self, text="Theme Editor", command=lambda: self.show_frogtool('e'), width=25, height=2)
        btn_7.pack(pady=10)

    def show_frogtool(self, version):
        """Mostrar la interfaz correspondiente (ImageProcessorAppSOP o ImageProcessorApp) dependiendo del parámetro."""
        if version == 'x':
            # Cambiar a ImageProcessorAppSOP
            self.master.change_frame(ImageProcessorAppSOP(self.master))
        elif version == 'e':
            # Cambiar a ImageProcessorApp
            self.master.change_frame(ImageProcessorApp(self.master))
