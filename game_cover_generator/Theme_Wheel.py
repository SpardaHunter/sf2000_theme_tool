import os
import tkinter as tk
from tkinter import filedialog, ttk, colorchooser, messagebox
from PIL import Image, ImageTk, ImageDraw, ImageFont
from natsort import natsorted  # Importar natsort para ordenación natural


class PhotoMergerApp(tk.Frame):
    def __init__(self, root):
        super().__init__(root)  # Llama al constructor de tk.Frame
        self.root = root

        # Configura el marco
        self.config(width=800, height=600)
        self.pack_propagate(False)

        # Variables
        self.bg_image_path = ""
        self.destination_folder = ""
        self.font_color = "red"
        self.font_name = "Arial"
        self.font_size = 20
        self.logos_folder = ""
        self.preview_window = None
        self.rectangles = {
            "logo": {"size": [75, 50], "position": [20, 225], "color": "red"},
            "next_logo1": {"size": [75, 50], "position": [20, 275], "color": "purple"},
            "next_logo2": {"size": [75, 50], "position": [20, 325], "color": "purple"},
            "next_logo3": {"size": [75, 50], "position": [20, 375], "color": "purple"},
            "next_logo4": {"size": [75, 50], "position": [20, 425], "color": "purple"},
            "next_logo5": {"size": [75, 50], "position": [100, 425], "color": "purple"},
            "next_logo6": {"size": [75, 50], "position": [175, 425], "color": "purple"},
            "next_logo7": {"size": [75, 50], "position": [250, 425], "color": "purple"},
            "prev_logo1": {"size": [75, 50], "position": [20, 175], "color": "green"},
            "prev_logo2": {"size": [75, 50], "position": [20, 125], "color": "green"},
            "prev_logo3": {"size": [75, 50], "position": [20, 75], "color": "green"},
            "prev_logo4": {"size": [75, 50], "position": [20, 25], "color": "green"},
            "prev_logo5": {"size": [75, 50], "position": [95, 25], "color": "green"},
            "prev_logo6": {"size": [75, 50], "position": [175, 25], "color": "green"},
            "prev_logo7": {"size": [75, 50], "position": [250, 25], "color": "green"},
            "screenshot": {"size": [150, 150], "position": [450, 50], "color": "blue"},
            "text": {"size": [200, 50], "position": [100, 225], "color": "orange"},
            "next_text1": {"size": [200, 50], "position": [100, 275], "color": "yellow"},
            "next_text2": {"size": [200, 50], "position": [100, 325], "color": "yellow"},
            "next_text3": {"size": [200, 50], "position": [100, 375], "color": "yellow"},
            "next_text4": {"size": [200, 50], "position": [350, 275], "color": "yellow"},
            "next_text5": {"size": [200, 50], "position": [350, 325], "color": "yellow"},
            "next_text6": {"size": [200, 50], "position": [350, 375], "color": "yellow"},
            "next_text7": {"size": [200, 50], "position": [350, 425], "color": "yellow"},
            "prev_text1": {"size": [200, 50], "position": [100, 175], "color": "pink"},
            "prev_text2": {"size": [200, 50], "position": [100, 125], "color": "pink"},
            "prev_text3": {"size": [200, 50], "position": [100, 75], "color": "pink"},
            "prev_text4": {"size": [200, 50], "position": [350, 25], "color": "pink"},
            "prev_text5": {"size": [200, 50], "position": [350, 75], "color": "pink"},
            "prev_text6": {"size": [200, 50], "position": [350, 125], "color": "pink"},
            "prev_text7": {"size": [200, 50], "position": [350, 175], "color": "pink"}
        }
        self.screenshots_folder = ""

        # Checkboxes para cambiar visibilidad
        self.visibility = {
            key: tk.BooleanVar(value=False) if key in ["prev_logo2","prev_logo3","prev_logo4","prev_logo5","prev_logo6","prev_logo7","next_logo2","next_logo3","next_logo4","next_logo5","next_logo6","next_logo7","prev_text1", "prev_text2", "prev_text3","prev_text4","prev_text5","prev_text6","prev_text7","next_text1","next_text2","next_text3","next_text4","next_text5","next_text6","next_text7"] else tk.BooleanVar(value=True)
            for key in self.rectangles.keys()
        }

        # Barra de progreso
        self.progress = tk.IntVar()

        # Crear interfaz
        self.create_interface()

    def choose_destination_folder(self):
        self.destination_folder = filedialog.askdirectory(title="Select Destination Folder")

    def choose_font_color(self):
        color_code = colorchooser.askcolor(title="Choose Font Color")[1]
        if color_code:
            self.font_color = color_code

    def choose_logos_folder(self):
        self.logos_folder = filedialog.askdirectory(title="Select Logos Folder")

    def choose_screenshots_folder(self):
        self.screenshots_folder = filedialog.askdirectory(title="Select Capture Folder")

    def create_interface(self):
        # title_label = tk.Label(self.root, text="Submenu Creator", font=("Arial", 18, "bold"))
        # title_label.grid(row=0, column=0, columnspan=2, pady=10)
    
        # Marco para botones principales
        button_frame = tk.Frame(self.root, bd=2, relief="groove", padx=10, pady=10)
        button_frame.grid(row=0, column=0, columnspan=2, pady=10, sticky="ew")
    
        # Modificar para colocar los botones en 2 columnas de 3 botones
        tk.Button(button_frame, text="1. Choose Background Image", command=self.open_preview_window, width=40).grid(row=0, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="2. Choose Capture Folder", command=self.choose_screenshots_folder, width=40).grid(row=0, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="3. Choose Logo Folder", command=self.choose_logos_folder, width=40).grid(row=1, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="4. Choose Destination Folder", command=self.choose_destination_folder, width=40).grid(row=1, column=1, padx=5, pady=5)
        tk.Button(button_frame, text="5. Unify", command=self.merge_images, width=40).grid(row=2, column=0, padx=5, pady=5)
        tk.Button(button_frame, text="6. Exit", command=self.root.quit, width=40).grid(row=2, column=1, padx=5, pady=5)
    
        # Controles para modificar tamaños de rectángulos y visibilidad
        size_frame = tk.LabelFrame(self.root, text="Modify Rectangles (Width x Height) & Toggle Elements", padx=10, pady=10)
        size_frame.grid(row=1, column=0, columnspan=2, pady=10, sticky="ew")
    
        self.size_entries = {}
        row = 0
        col = 0
        for i, (key, rect) in enumerate(self.rectangles.items()):
            tk.Label(size_frame, text=key.capitalize()).grid(row=row, column=col, padx=5, pady=5)
    
            width_entry = tk.Entry(size_frame, width=5)
            width_entry.insert(0, rect["size"][0])
            width_entry.grid(row=row, column=col + 1, padx=5)
    
            height_entry = tk.Entry(size_frame, width=5)
            height_entry.insert(0, rect["size"][1])
            height_entry.grid(row=row, column=col + 2, padx=5)
    
            tk.Button(size_frame, text="Update", command=lambda k=key, w=width_entry, h=height_entry: self.update_rectangle_size(k, w, h)).grid(row=row, column=col + 3, padx=5)
    
            self.size_entries[key] = (width_entry, height_entry)
    
            # Checkbox para la visibilidad
            visibility_checkbox = tk.Checkbutton(size_frame, variable=self.visibility[key], command=self.update_visibility)
            visibility_checkbox.grid(row=row, column=col + 4, padx=5, pady=5, sticky="w")
    
            col += 5
            if col >= 20:  # Cambiar cuando se llegue al final de una fila con 5 columnas
                col = 0
                row += 1
    
        # Botones para cambiar fuente y color
        font_frame = tk.LabelFrame(self.root, text="Font Settings", padx=10, pady=10)
        font_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="ew")
    
        tk.Label(font_frame, text="Font:").grid(row=0, column=0, padx=5)
        self.font_menu = ttk.Combobox(font_frame, values=["Arial", "Courier", "Times New Roman", "Verdana"])
        self.font_menu.set("Arial")
        self.font_menu.grid(row=0, column=1, padx=5)
    
        tk.Label(font_frame, text="Size:").grid(row=0, column=2, padx=5)
        self.font_size_entry = tk.Entry(font_frame, width=5)
        self.font_size_entry.insert(0, "20")
        self.font_size_entry.grid(row=0, column=3, padx=5)
    
        tk.Button(font_frame, text="Set Font", command=self.set_font).grid(row=0, column=4, padx=5)
        tk.Button(font_frame, text="Set Color", command=self.choose_font_color).grid(row=0, column=5, padx=5)
    
        # Barra de progreso
        self.progress_bar = ttk.Progressbar(self.root, orient="horizontal", length=400, mode="determinate", variable=self.progress)
        self.progress_bar.grid(row=3, column=0, columnspan=2, pady=20, sticky="ew")

    def merge_images(self):
        if not self.bg_image_path:
            tk.messagebox.showwarning("Warning", "You must select a background image before merging.")
            return
        if not self.screenshots_folder:
            tk.messagebox.showwarning("Warning", "You must select a capture folder before merging.")
            return
        if not self.logos_folder:
            tk.messagebox.showwarning("Warning", "You must select a logo folder before merging.")
            return
        if not self.destination_folder:
            tk.messagebox.showwarning("Warning", "You must select a destination folder before merging.")
            return

        try:
            bg_image = Image.open(self.bg_image_path).resize((640, 480))
            
            # Utilizar natsorted para ordenar los archivos de manera natural (números y caracteres especiales)
            screenshots = natsorted(os.listdir(self.screenshots_folder))
            logos = natsorted(os.listdir(self.logos_folder))

            # Configurar barra de progreso
            total_files = len(screenshots)
            self.progress.set(0)
            self.progress_bar.config(maximum=total_files)

            for i, screenshot_name in enumerate(screenshots):
                screenshot_path = os.path.join(self.screenshots_folder, screenshot_name)

                # Determinar el logo previo y siguiente
                logo_prev_name = logos[-1] if i == 0 else logos[i - 1]
                logo_next_name = logos[0] if i == len(logos) - 1 else logos[i + 1]
                logo_prev_path = os.path.join(self.logos_folder, logo_prev_name)
                logo_next_path = os.path.join(self.logos_folder, logo_next_name)
                logo_path = os.path.join(self.logos_folder, screenshot_name)

                try:
                    screenshot = Image.open(screenshot_path).resize(tuple(self.rectangles["screenshot"]["size"]))
                except FileNotFoundError:
                    continue

                combined = bg_image.copy()
                if self.visibility["screenshot"].get():
                    combined.paste(screenshot, tuple(self.rectangles["screenshot"]["position"]), screenshot if screenshot.mode == "RGBA" else None)

                if self.visibility["logo"].get():
                    try:
                        logo = Image.open(logo_path).resize(tuple(self.rectangles["logo"]["size"])).convert("RGBA")
                        combined.paste(logo, tuple(self.rectangles["logo"]["position"]), logo)
                    except FileNotFoundError:
                        pass

                # Procesar todos los "prev_logo" y "next_logo"
                for j in range(1, 7):  # Itera de 1 a 7
                    key = f"prev_logo{j}"
                    if self.visibility[key].get():
                        try:
                            prev_logo_index = (i - j) % len(logos)  # Índice del logo previo cíclico
                            prev_logo_name = logos[prev_logo_index]
                            prev_logo_path = os.path.join(self.logos_folder, prev_logo_name)
                            prev_logo = Image.open(prev_logo_path).resize(tuple(self.rectangles[key]["size"])).convert("RGBA")
                            combined.paste(prev_logo, tuple(self.rectangles[key]["position"]), prev_logo)
                        except FileNotFoundError:
                            pass

                # Procesar todos los "next_logo" adicionales
                for j in range(1, 7):  # Itera de 1 a 7
                    key = f"next_logo{j}"
                    if self.visibility[key].get():
                        try:
                            next_logo_index = (i + j) % len(logos)  # Índice del logo siguiente cíclico
                            next_logo_name = logos[next_logo_index]
                            next_logo_path = os.path.join(self.logos_folder, next_logo_name)
                            next_logo = Image.open(next_logo_path).resize(tuple(self.rectangles[key]["size"])).convert("RGBA")
                            combined.paste(next_logo, tuple(self.rectangles[key]["position"]), next_logo)
                        except FileNotFoundError:
                            pass

                if self.visibility["text"].get():
                    draw = ImageDraw.Draw(combined)
                    font = ImageFont.truetype("arial.ttf", self.font_size)
                    text_position = tuple(self.rectangles["text"]["position"])
                    draw.text(text_position, screenshot_name.rsplit(".", 1)[0], font=font, fill=self.font_color)

                # Para los "prev_text1", "prev_text2", ..., "prev_text7" (logos anteriores)
                for j in range(1, 7):  # Itera de 1 a 7
                    if self.visibility[f"prev_text{j}"].get():
                        prev_text_position = tuple(self.rectangles[f"prev_text{j}"]["position"])
                        prev_text_index = (i - j) % len(logos)  # Cálculo cíclico
                        prev_text_name = logos[prev_text_index]
                        prev_text = os.path.splitext(prev_text_name)[0]  # Nombre sin extensión
                        draw.text(prev_text_position, prev_text, font=font, fill=self.font_color)

                # Para los "next_text1", "next_text2", ..., "next_text7" (logos siguientes)
                for j in range(1, 7):  # Itera de 1 a 7
                    if self.visibility[f"next_text{j}"].get():
                        next_text_position = tuple(self.rectangles[f"next_text{j}"]["position"])
                        next_text_index = (i + j) % len(logos)  # Cálculo cíclico
                        next_text_name = logos[next_text_index]
                        next_text = os.path.splitext(next_text_name)[0]  # Nombre sin extensión
                        draw.text(next_text_position, next_text, font=font, fill=self.font_color)

                output_path = os.path.join(self.destination_folder, screenshot_name)
                combined.save(output_path)

                self.progress.set(i + 1)
                self.root.update_idletasks()

            tk.messagebox.showinfo("Process Completed", "The images have been successfully unified.")
        except Exception as e:
            tk.messagebox.showerror("Error", f"An error occurred during processing: {str(e)}")



    def open_preview_window(self):
        self.bg_image_path = filedialog.askopenfilename(
            title="Select Background Image",
            filetypes=[("Image Files", "*.png;*.jpg;*.jpeg")]
        )

        if not self.bg_image_path:
            tk.messagebox.showwarning("Warning", "No background image selected.")
            return

        if self.preview_window is not None:
            self.preview_window.destroy()

        self.preview_window = tk.Toplevel(self.root)
        self.preview_window.title("Preview")
        self.preview_window.geometry("800x700")

        self.canvas = tk.Canvas(self.preview_window, width=640, height=480, bg="gray")
        self.canvas.pack(pady=20)

        bg_image = Image.open(self.bg_image_path).resize((640, 480))
        self.bg_image_tk = ImageTk.PhotoImage(bg_image)
        self.canvas.create_image(0, 0, anchor="nw", image=self.bg_image_tk)

        self.rect_ids = {}
        for key, rect in self.rectangles.items():
            if self.visibility[key].get():
                x, y = rect["position"]
                w, h = rect["size"]
                color = rect["color"]
                self.rect_ids[key] = self.canvas.create_rectangle(x, y, x + w, y + h, outline=color, width=2, tags=key)

                # Permitir mover los rectángulos
                self.canvas.tag_bind(key, "<B1-Motion>", lambda event, key=key: self.move_rect(self.canvas, key, event))

    def move_rect(self, canvas, rect_type, event):
        x0, y0, x1, y1 = canvas.coords(self.rect_ids[rect_type])
        width = x1 - x0
        height = y1 - y0
        new_x0 = max(min(event.x, 640 - width), 0)
        new_y0 = max(min(event.y, 480 - height), 0)
        canvas.coords(self.rect_ids[rect_type], new_x0, new_y0, new_x0 + width, new_y0 + height)

        # Actualizar posición
        self.rectangles[rect_type]["position"] = [new_x0, new_y0]

    def set_font(self):
        self.font_name = self.font_menu.get()
        try:
            self.font_size = int(self.font_size_entry.get())
        except ValueError:
            tk.messagebox.showerror("Error", "Font size must be an integer.")

    def update_rectangle_size(self, rect_key, width_entry, height_entry):
        try:
            width = int(width_entry.get())
            height = int(height_entry.get())

            if width > 0 and height > 0:
                self.rectangles[rect_key]["size"] = [width, height]
                if self.preview_window and self.canvas and rect_key in self.rect_ids:
                    x0, y0 = self.rectangles[rect_key]["position"]
                    self.canvas.coords(self.rect_ids[rect_key], x0, y0, x0 + width, y0 + height)
            else:
                tk.messagebox.showwarning("Invalid Size", "Width and height must be positive integers.")
        except ValueError:
            tk.messagebox.showerror("Error", "Please enter valid integers for width and height.")

    def update_visibility(self):
        if self.preview_window and self.canvas:
            for key, visible in self.visibility.items():
                if key in self.rect_ids:
                    if visible.get():
                        self.canvas.itemconfigure(self.rect_ids[key], state="normal")
                    else:
                        self.canvas.itemconfigure(self.rect_ids[key], state="hidden")


if __name__ == "__main__":
    root = tk.Tk()
    app = PhotoMergerApp(root)
    root.mainloop()