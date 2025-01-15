import tkinter as tk
import subprocess

class GameListUpdater(tk.Frame):
    def __init__(self, root):
        super().__init__(root)

        # Etiqueta de título
        self.label = tk.Label(self, text="Game List Updater Module")
        self.label.pack(pady=20)

        # Botón para abrir el programa relacionado con FoldernamX.ini
        btn_12 = tk.Button(self, text="FoldernamX.ini", command=lambda: self.open_tool('game_list_updater/foldernamx.py'), width=25, height=2)
        btn_12.pack(pady=10)

        # Botón para abrir el programa relacionado con Foldername.ini
        btn_7 = tk.Button(self, text="Foldername.ini", command=lambda: self.open_tool('game_list_updater/foldername.py'), width=25, height=2)
        btn_7.pack(pady=10)

        # Inicializar el proceso
        self.current_process = None

    def open_tool(self, script_path):
        """Abrir un programa sin bloquear la GUI y cerrar cualquier proceso existente."""
        # Cerrar el proceso en ejecución si existe
        if self.current_process and self.current_process.poll() is None:
            try:
                self.current_process.terminate()
                self.current_process.wait(timeout=5)
            except Exception:
                self.current_process.kill()

        # Abrir el nuevo programa
        self.current_process = subprocess.Popen(['python', script_path], shell=False)
