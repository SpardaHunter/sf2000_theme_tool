import os
import struct
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image
from collections import namedtuple

class ZFBimagesTool(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        # --- Tamaños de imagen ---
        self.ImageSize = namedtuple('ImageSize', [
            "full_width", "full_height", 
            "default_width", "default_height", 
            "init_width", "init_height"
        ])
        self.img = self.ImageSize(
            full_width="640", full_height="480", 
            default_width="144", default_height="208", 
            init_width="640", init_height="480"
        )

        # Crear la interfaz
        self.create_widgets()

    def create_widgets(self):
        # Fuentes
        bold_font = ("Helvetica", 10, "bold")
        label_font = ("Helvetica", 10, "normal")

        # Input Folder
        self.create_label_entry(
            row=1, label_text="Input Folder:", var_name="input_folder_var", 
            button_text="Browse", button_command=self.select_input_folder, label_font=label_font
        )

        # Output Folder
        self.create_label_entry(
            row=2, label_text="Output Folder:", var_name="output_folder_var", 
            button_text="Browse", button_command=self.select_output_folder, label_font=label_font
        )

        # Core y Extension
        self.create_core_and_extension(label_font)

        # Tamaño de imagen
        self.create_image_size_widgets(label_font)

        # Botón para crear archivos ZFB
        self.create_zfb_button = tk.Button(
            self.master, text="Create ZFB Files", command=self.create_zfb_files, font=("Helvetica", 14)
        )
        self.create_zfb_button.grid(row=6, column=0, columnspan=7, pady=10)

        # Mensajes de estado
        self.msg_var = tk.StringVar()
        tk.Label(self.master, textvariable=self.msg_var, font=label_font).grid(row=7, column=0, columnspan=7, sticky="w", padx=10)

        # Inicialización de valores predeterminados
        c_dir = os.path.dirname(os.path.abspath(__file__))
        self.input_folder_var.set(c_dir)
        self.output_folder_var.set(os.path.join(c_dir, "output"))
        self.imgwidth_var.set(self.img.init_width)
        self.imgheight_var.set(self.img.init_height)

        # Configuración del grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_columnconfigure(2, weight=1)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
        self.grid_rowconfigure(5, weight=1)

        # Atajos de teclado
        self.core_entry.bind("<Return>", self.entry_enter_key)
        self.extension_entry.bind("<Return>", self.entry_enter_key)
        self.create_zfb_button.bind("<Return>", self.entry_enter_key)
        self.core_entry.focus_set()

    def create_label_entry(self, row, label_text, var_name, button_text, button_command, label_font):
        tk.Label(self.master, text=label_text, font=label_font).grid(row=row, column=0, sticky="w", padx=10)
        
        var = tk.StringVar()
        setattr(self, var_name, var)

        entry = tk.Entry(self.master, textvariable=var, width=70)
        setattr(self, f"{var_name}_entry", entry)
        entry.grid(row=row, column=1, columnspan=5, sticky="w", padx=5)

        button = tk.Button(self.master, text=button_text, command=button_command)
        setattr(self, f"{var_name}_button", button)
        button.grid(row=row, column=6, sticky="w")

    def create_core_and_extension(self, label_font):
        # Core
        self.core_var = tk.StringVar()
        self.core_var.trace_add("write", self.core_input_callback)
        tk.Label(self.master, text="CORE:", font=label_font).grid(row=3, column=0, sticky="w", padx=10)
        self.core_entry = tk.Entry(self.master, textvariable=self.core_var, width=10)
        self.core_entry.grid(row=3, column=1, sticky="w", padx=5)

        # Extension
        self.extension_var = tk.StringVar()
        tk.Label(self.master, text="EXTENSION:", font=label_font).grid(row=3, column=2, sticky="w", padx=5)
        self.extension_entry = tk.Entry(self.master, textvariable=self.extension_var, width=10)
        self.extension_entry.grid(row=3, column=3, sticky="w", padx=5)

    def create_image_size_widgets(self, label_font):
        self.imgwidth_var = tk.StringVar()
        self.imgheight_var = tk.StringVar()
        self.img_fullscreen_var = tk.BooleanVar(value=True)

        tk.Label(self.master, text="Image Size:", font=label_font).grid(row=5, column=0, sticky="w", padx=10)
        tk.Entry(self.master, textvariable=self.imgwidth_var, width=10).grid(row=5, column=1, sticky="w", padx=5)
        tk.Label(self.master, text="x", font=label_font).grid(row=5, column=2, sticky="w")
        tk.Entry(self.master, textvariable=self.imgheight_var, width=10).grid(row=5, column=3, sticky="w", padx=5)

        tk.Checkbutton(self.master, variable=self.img_fullscreen_var, command=self.change_fullscreen_state).grid(row=5, column=4, sticky="e")
        tk.Label(self.master, text="Fullscreen mode", font=label_font).grid(row=5, column=5, sticky="w")

    def change_fullscreen_state(self):
        if self.img_fullscreen_var.get():
            self.imgwidth_var.set(self.img.full_width)
            self.imgheight_var.set(self.img.full_height)
        else:
            self.imgwidth_var.set(self.img.default_width)
            self.imgheight_var.set(self.img.default_height)

    def entry_enter_key(self, event):
        if event.keysym == "Return":
            if event.widget == self.core_entry:
                self.extension_entry.focus_set()
            elif event.widget == self.extension_entry:
                self.create_zfb_button.focus_set()
            elif event.widget == self.create_zfb_button:
                self.create_zfb_files()

    def core_input_callback(self, *args):
        self.extension_var.set(self.core_var.get())

    def select_input_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.input_folder_var.set(folder_path)

    def select_output_folder(self):
        folder_path = filedialog.askdirectory()
        if folder_path:
            self.output_folder_var.set(folder_path)

    def create_zfb_files(self):
        try:
            input_folder = self.input_folder_var.get()
            output_folder = self.output_folder_var.get()
            core = self.core_var.get()
            extension = self.extension_var.get()
            
            img_w = self.imgwidth_var.get()
            img_h = self.imgheight_var.get()

            if not input_folder or not output_folder or not core or not extension or not img_w or not img_h:
                messagebox.showwarning('Warning', 'Please fill in all the fields and select input and output folders.')
                return

            if not os.path.exists(output_folder):
                os.makedirs(output_folder)

            thumb_size = (int(img_w), int(img_h))
            self.msg_var.set("Processing ... ")
            self.create_zfb_button["state"] = "disabled"
            self.master.update()

            for file_name in os.listdir(input_folder):
                file_path = os.path.join(input_folder, file_name)
                try:
                    with Image.open(file_path) as img:
                        img = img.resize(thumb_size).convert("RGB")
                        raw_data = [
                            struct.pack('H', ((r >> 3) << 11) | ((g >> 2) << 5) | (b >> 3))
                            for y in range(thumb_size[1])
                            for x in range(thumb_size[0])
                            for r, g, b in [img.getpixel((x, y))]
                        ]
                        zfb_filename = os.path.join(output_folder, os.path.splitext(file_name)[0] + '.zfb')
                        with open(zfb_filename, 'wb') as zfb:
                            zfb.write(b''.join(raw_data))
                            zfb.write(b'\x00\x00\x00\x00')
                            zfb.write(f"{core};{os.path.splitext(file_name)[0]}.{extension}.gba".encode('utf-8'))
                            zfb.write(b'\x00\x00')
                except:
                    placeholder = b'\x00' * 0xEA00 + b'\x00\x00\x00\x00' + f"{core};{os.path.splitext(file_name)[0]}.gba".encode('utf-8') + b'\x00\x00'
                    with open(os.path.join(output_folder, os.path.splitext(file_name)[0] + '.zfb'), 'wb') as zfb:
                        zfb.write(placeholder)

            self.msg_var.set("")
            messagebox.showinfo('Success', 'ZFB files created successfully.')
        except Exception as e:
            messagebox.showerror('Error', f'An error occurred: {str(e)}')
        self.create_zfb_button["state"] = "normal"

if __name__ == "__main__":
    root = tk.Tk()
    root.geometry("640x260")
    root.resizable(False, False)
    root.title("ZFB Generator")
    app = ZFBimagesTool(master=root)
    root.mainloop()
