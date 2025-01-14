import tkinter as tk
from PIL import Image, ImageTk
from tkinter import messagebox, filedialog

class MenuImageGenerator(tk.Frame):

    def __init__(self, root):
        super().__init__(root)
        self.img_width = 576
        self.img_height = 168

        self.preview_width = self.img_width // 3
        self.preview_height = self.img_height // 3

        self.export_path = ""
        self.images = []
        self.previews = []
        self.image_buttons = []

        self.preview_window = MenuImagePreview(self)

        self.initialize_images()

        self.button_frame = tk.Frame(self)
        self.button_frame.grid(row=0, column=0, padx=5, pady=5, sticky="nsew")

        self.selected_option = tk.IntVar(value=8)
        tk.Label(self.button_frame, text="Number of images:").grid(row=0, column=0, padx=5, pady=5, sticky="e")

        self.option_menu = tk.OptionMenu(self.button_frame, self.selected_option, *range(1, 14), command=lambda _: self.update_previews())
        self.option_menu.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        for i in range(13):
            btn = tk.Button(self.button_frame, text=f"Image {i+1}", command=lambda i=i: self.load_image(i))
            self.image_buttons.append(btn)
            if i < 8:  # Show the first 8 buttons initially
                btn.grid(row=i + 1, column=0, columnspan=2, pady=2)

        self.destination_label = tk.Label(self.button_frame, text="Destination: Not selected", anchor="w")
        self.destination_label.grid(row=14, column=0, columnspan=2, padx=5, pady=5, sticky="w")
        tk.Button(self.button_frame, text="Select destination", command=self.select_destination).grid(row=15, column=0, columnspan=2, pady=5)

        tk.Button(self.button_frame, text="Export", command=self.export_images, bg="green", fg="white").grid(row=16, column=0, columnspan=2, pady=10)

        self.update_previews()

    def create_transparent_image(self):
        """Creates a transparent image."""
        return Image.new("RGBA", (self.img_width, self.img_height), (0, 0, 0, 0))

    def update_previews(self):
        """Updates preview images and buttons."""
        total_images = self.selected_option.get()  # Number of selected images
        for i in range(13):
            preview_img = self.images[i].resize((self.preview_width, self.preview_height), Image.Resampling.LANCZOS)
            preview_photo = ImageTk.PhotoImage(preview_img)
            self.previews[i].config(image=preview_photo)
            self.previews[i].image = preview_photo
            self.previews[i].pack_forget() if i >= total_images else self.previews[i].pack(pady=2)
            if i < total_images:
                self.image_buttons[i].grid(row=i + 1, column=0, columnspan=2, pady=2)
            else:
                self.image_buttons[i].grid_forget()

    def initialize_images(self):
        """Initializes images with default transparency."""
        self.images = [self.create_transparent_image() for _ in range(13)]
        self.previews = []
        for i in range(13):
            self.preview_img = self.images[i].resize((self.preview_width, self.preview_height), Image.Resampling.LANCZOS)
            self.preview_photo = ImageTk.PhotoImage(self.preview_img)
            self.preview_label = tk.Label(self.preview_window.preview_frame, image=self.preview_photo)
            self.preview_label.image = self.preview_photo
            self.preview_label.pack(pady=2)
            self.previews.append(self.preview_label)

    def load_image(self, index):
        """Loads an image at the specified position."""
        filepath = filedialog.askopenfilename()
        if not filepath:
            return

        try:
            img = Image.open(filepath).convert("RGBA")
            img = img.resize((self.img_width, self.img_height), Image.Resampling.LANCZOS)
            self.images[index] = img
            self.update_previews()
        except Exception as e:
            messagebox.showerror("Error", f"The image could not be loaded: {e}")

    def select_destination(self):
        """Selects the export destination folder."""
        global export_path
        export_path = filedialog.askdirectory()
        if export_path:
            self.destination_label.config(text=f"Destination: {export_path}")

    def export_images(self):
        """Exports the combined images."""
        if not export_path:
            messagebox.showerror("Error", "Please select a destination.")
            return

        total_images = self.selected_option.get()
        canvas_height = total_images * self.img_height

        composite = Image.new("RGBA", (self.img_width, canvas_height), (0, 0, 0, 0))

        for i in range(total_images):
            if self.images[i]:
                composite.paste(self.images[i], (0, i * self.img_height))

        output_file = f"{export_path}/sfcdr.cpl.png"
        try:
            composite.save(output_file)
            messagebox.showinfo("Success", f"Image exported to {output_file}")
        except Exception as e:
            messagebox.showerror("Error", f"Could not export image: {e}")

class MenuImagePreview(tk.Toplevel):

    def __init__(self, root):
        super().__init__(root)

        self.title("Preview")
        self.geometry(f"{self.master.preview_width+40}x{self.master.preview_height*8+40}")

        self.preview_canvas = tk.Canvas(self)
        self.scrollbar = tk.Scrollbar(self, orient="vertical", command=self.preview_canvas.yview)
        self.preview_canvas.configure(yscrollcommand=self.scrollbar.set)

        self.scrollbar.pack(side="right", fill="y")
        self.preview_canvas.pack(side="left", fill="both", expand=True)

        self.preview_frame = tk.Frame(self.preview_canvas)
        self.preview_canvas.create_window((0, 0), window=self.preview_frame, anchor="nw")
        self.preview_frame.bind("<Configure>", self.configure_scroll)

    def configure_scroll(self, event):
        self.preview_canvas.configure(scrollregion=self.preview_canvas.bbox("all"))

if __name__ == '__main__':
    root = tk.Tk()
    root.title("Menu Image Generator")
    root.geometry("800x600")
    frame = MenuImageGenerator(root)
    frame.grid(row=0, column=0, sticky='nsew')
    root.mainloop()
