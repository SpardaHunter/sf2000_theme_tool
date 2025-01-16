import tkinter as tk
from menu_image_generator.menu_image_generator import MenuImageGenerator
from game_list_updater.game_list_updater import GameListUpdater
from game_list_updater.foldernamx import FrogtoolGUIx
from game_list_updater.foldername import FrogtoolGUIe
from zfb_generator.zfb_generator import ZFBGenerator
from zfb_generator.ZFBimagesTool import ZFBimagesTool

class SF2000ThemeTool(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title('SF2000 Theme Tool')
        self.geometry('800x600')

        self.menu = SideMenu(self)
        self.menu.grid(row=0, column=0, sticky='nswe', padx=0, pady=0)

        self.tool = Home(self)
        self.tool.config(bd=2, relief='solid')
        self.tool.grid(row=0, column=1, sticky="nswe", padx=3, pady=0)

        self.grid_columnconfigure(0, weight=1, minsize=200)
        self.grid_columnconfigure(1, weight=3, minsize=600)
        self.grid_rowconfigure(0, weight=1, minsize=600)

        self.current_frame_process = None

    def change_frame(self, tool: tk.Frame):
        # Cerrar cualquier proceso en ejecución
        if self.current_frame_process and hasattr(self.current_frame_process, 'current_process'):
            process = self.current_frame_process.current_process
            if process:
                try:
                    process.terminate()  # Intentar cerrar el proceso
                    process.wait(timeout=5)  # Esperar a que se cierre
                except Exception:
                    process.kill()  # Forzar el cierre si no responde

        # Cambiar el marco
        self.tool.destroy()
        self.tool = tool
        self.tool.config(bd=2, relief='solid')
        self.tool.grid(row=0, column=1, sticky="nswe", padx=3, pady=0)

        # Actualizar referencia al nuevo marco
        self.current_frame_process = tool


class SideMenu(tk.Frame):
    def __init__(self, root):
        super().__init__(master=root)
        self.menu_buttons = {
            'home': 'Home',
            'game_list_updater': 'Game List Updater',
            'game_cover_generator': 'Game Cover Generator',
            'menu_image_generator': 'Menu Image Generator',
            'theme_image_generator': 'Theme Image Generator',
            'zfb_generator': 'ZFB Generator'
        }

        button_position = 0
        for tool, title in self.menu_buttons.items():
            button = tk.Button(self, text=title, command=lambda t=tool: self.change_tool(t))
            button.grid(row=button_position, column=0, sticky='ew')
            button_position += 1

    def change_tool(self, tool):
        match tool:
            case 'game_list_updater':
                self.master.change_frame(GameListUpdater(self.master))
            case 'game_cover_generator':
                self.master.change_frame(GameCoverGenerator(self.master))
            case 'menu_image_generator':
                self.master.change_frame(MenuImageGenerator(self.master))
            case 'theme_image_generator':
                self.master.change_frame(ThemeImageGenerator(self.master))
            case 'zfb_generator':
                self.master.change_frame(ZFBGenerator(self.master))
            case _:
                self.master.change_frame(Home(self.master))

class Home(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.label = tk.Label(self, text="Bienvenido a la aplicación")
        self.label.pack(pady=20)

class GameCoverGenerator(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.label = tk.Label(self, text="Game Cover Generator")
        self.label.pack(pady=20)

class ThemeImageGenerator(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.label = tk.Label(self, text="Theme Image Generator")
        self.label.pack(pady=20)

if __name__ == '__main__':
    app = SF2000ThemeTool()
    app.mainloop()
