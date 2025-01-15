import tkinter as tk
from game_list_updater.foldernamx import FrogtoolGUIx
from game_list_updater.foldername import FrogtoolGUIe

class GameListUpdater(tk.Frame):
    def __init__(self, root):
        super().__init__(root)

        # Etiqueta de título
        self.label = tk.Label(self, text="Game List Updater Module")
        self.label.pack(pady=20)

        # Botón para mostrar la clase FrogtoolGUIx
        btn_12 = tk.Button(self, text="FoldernamX.ini", command=lambda: self.show_frogtool('x'), width=25, height=2)
        btn_12.pack(pady=10)

        # Botón para mostrar la clase FrogtoolGUIe
        btn_7 = tk.Button(self, text="Foldername.ini", command=lambda: self.show_frogtool('e'), width=25, height=2)
        btn_7.pack(pady=10)

    def show_frogtool(self, version):
        """Mostrar la interfaz correspondiente (FrogtoolGUIx o FrogtoolGUIe) dependiendo del parámetro."""
        if version == 'x':
            # Cambiar a FrogtoolGUIx
            self.master.change_frame(FrogtoolGUIx(self.master))
        elif version == 'e':
            # Cambiar a FrogtoolGUIe
            self.master.change_frame(FrogtoolGUIe(self.master))
