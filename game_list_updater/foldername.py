import os
import re
import binascii
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import psutil

class StopExecution(Exception):
    pass


class FrogtoolGUIe(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.grid(row=0, column=0, sticky="nswe")  # Asegúrate de usar grid aquí

        self.drive_combobox = None
        self.path_entry = None
        self.custom_path_var = tk.BooleanVar()
        self.system_var = tk.StringVar(root)
        self.system_var.set("ALL")
        self.system_menu = None

        self.systems = {
            "FC": ["rdbui.tax", "fhcfg.nec", "nethn.bvs"],
            "SFC":     ["urefs.tax", "adsnt.nec", "xvb6c.bvs"],
            "MD":     ["scksp.tax", "setxa.nec", "wmiui.bvs"],
            "GB":    ["vdsdc.tax", "umboa.nec", "qdvd6.bvs"],
            "GBC":    ["pnpui.tax", "wjere.nec", "mgdel.bvs"],
            "GBA":     ["vfnet.tax", "htuiw.nec", "sppnp.bvs"],
            "ARCADE":    ["mswb7.tax", "msdtc.nec", "mfpmp.bvs"],
            "ALL": []  # Placeholder for "ALL" option
        }
        self.supported_rom_ext = [
            "bkp", "zip", "zfc", "zsf", "zmd", "zgb", "zfb", "smc", "fig", "sfc", "gd3", "gd7", "dx2", "bsx", "swc", "nes",
            "nfc", "fds", "unf", "gba", "agb", "gbz", "gbc", "gb", "sgb", "bin", "md", "smd", "gen", "sms"
        ]

        self.setup_gui()



    def setup_gui(self):
        # Etiquetas y botones para la UI
        drive_label = tk.Label(self, text="SF2000 SD Card Location:")
        self.drive_combobox = ttk.Combobox(self, state="readonly", width=37)
        self.drive_combobox.bind("<<ComboboxSelected>>", self.on_drive_selected)

        custom_path_checkbox = ttk.Checkbutton(self, text="Use Custom Path", variable=self.custom_path_var)
        path_label = tk.Label(self, text="Custom Path:")
        self.path_entry = ttk.Entry(self, width=40)
        path_button = ttk.Button(self, text="Browse", command=self.select_folder)

        system_label = tk.Label(self, text="Select System:")
        self.system_menu = tk.OptionMenu(self, self.system_var, *self.systems.keys())

        execute_button = tk.Button(self, text="Update Games List", command=self.execute_conversion)

        # Usamos grid() en lugar de pack() para todo
        drive_label.grid(row=0, column=0, pady=5)
        self.drive_combobox.grid(row=0, column=1, pady=5)
        custom_path_checkbox.grid(row=1, column=0, columnspan=2, pady=5)
        path_label.grid(row=2, column=0, pady=5)
        self.path_entry.grid(row=2, column=1, pady=5)
        path_button.grid(row=2, column=2, pady=5)
        system_label.grid(row=3, column=0, pady=5)
        self.system_menu.grid(row=3, column=1, pady=5)
        execute_button.grid(row=4, column=0, columnspan=2, pady=10)
    
        self.grid_columnconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=3)
        self.grid_rowconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)
        self.grid_rowconfigure(2, weight=1)
        self.grid_rowconfigure(3, weight=1)
        self.grid_rowconfigure(4, weight=1)
    
        # Inicializamos la búsqueda de drives después de que la ventana se muestre
        self.root.after(100, self.browse_drive)


    def browse_drive(self):
        drives = [drive.device for drive in psutil.disk_partitions()] if os.name == "nt" else [drive.mountpoint for drive in psutil.disk_partitions()]
        self.drive_combobox['values'] = drives
        if drives:
            self.drive_combobox.set(drives[0])

    def on_drive_selected(self, event):
        if not self.custom_path_var.get():  # Solo busca automáticamente si el checkbox está desactivado
            self.check_and_find_ini()

    def select_folder(self):
        folder_selected = filedialog.askdirectory(title="Select Folder")
        if folder_selected:
            self.path_entry.delete(0, tk.END)
            self.path_entry.insert(0, folder_selected)
            self.check_and_find_ini()

    def check_and_find_ini(self):
        path = self.path_entry.get() if self.custom_path_var.get() else self.drive_combobox.get()
        if path:
            self.find_foldername_ini(path)

    def find_foldername_ini(self, path):
        ini_path = os.path.join(path, "Resources", "Foldername.ini")
        if not os.path.exists(ini_path):
            messagebox.showerror("Error", f"File not found: {ini_path}")
            return
    
        try:
            with open(ini_path, "r", encoding="utf-8") as file:
                lines = file.readlines()
    
            if len(lines) < 3:
                messagebox.showerror("Error", f"Insufficient lines in {ini_path}")
                return
    
            last_number_line = lines[-3].strip().split()[0]
            try:
                num_lines = int(last_number_line) - 1
            except ValueError:
                messagebox.showerror("Error", f"Invalid number format in antepenultimate line: {last_number_line}")
                return
    
            if len(lines) < num_lines + 4:
                messagebox.showerror("Error", f"Not enough lines in {ini_path} to process {num_lines}.")
                return
    
            new_keys = []
            for line in lines[4:4 + num_lines]:
                parts = line.strip().split(" ", 1)
                key = parts[1] if len(parts) > 1 else parts[0]
                new_keys.append(key)
    
            updated_systems = dict(zip(new_keys, self.systems.values()))
            self.systems = updated_systems
    
            self.systems["ALL"] = []
    
            menu = self.system_menu["menu"]
            menu.delete(0, "end")
            for key in self.systems.keys():
                menu.add_command(label=key, command=tk._setit(self.system_var, key))
    
            self.system_var.set("ALL")
            messagebox.showinfo("Success", "Systems updated successfully from Foldername.ini!")
            print("Updated systems:", self.systems)
    
        except Exception as e:
            messagebox.showerror("Error", f"Failed to read or process {ini_path}: {e}")


    def execute_conversion(self):
        path = self.path_entry.get() if self.custom_path_var.get() else self.drive_combobox.get()
        system = self.system_var.get()

        if not path:
            messagebox.showerror("Error", "No path has been selected.")
            return

        if system == "ALL":
            keys_to_process = [key for key in self.systems.keys() if key != "ALL"]
        else:
            keys_to_process = [system]

        try:
            for syskey in keys_to_process:
                self.process_sys(path, syskey)
            messagebox.showinfo("Message", "Updated games list!")
        except StopExecution:
            print("Error updating game list.")

    def process_sys(self, path, system):
        # Implementación del procesamiento del sistema
        pass

def check_and_find_ini():
    global custom_path_var, path_entry, drive_combobox, systems
    if custom_path_var.get():
        path = path_entry.get()
        if path:
            find_foldername_ini(path)
    else:
        path = drive_combobox.get()
        if path:
            find_foldername_ini(path)

def check_file(file_entry, supported_exts):
    file_regex = ".+\\.(" + "|".join(supported_exts) + ")$"
    return file_entry.is_file() and re.search(file_regex, file_entry.name.lower())

def check_rom(file_entry):
    return check_file(file_entry, supported_rom_ext)

def strip_file_extension(name):
    parts = name.split(".")
    parts.pop()
    return ".".join(parts)

def sort_normal(unsorted_list):
    return sorted(unsorted_list)

def sort_without_file_ext(unsorted_list):
    stripped_names = list(map(strip_file_extension, unsorted_list))
    sort_map = dict(zip(unsorted_list, stripped_names))
    return sorted(sort_map, key=sort_map.get)

def process_sys(path, system):
    print(f"Processing {system}")

    if not path:
        messagebox.showerror("Error", "No path has been selected.")
        return

    roms_path = os.path.join(path, system)
    if not os.path.isdir(roms_path):
        os.makedirs(os.path.join(roms_path, "save"), exist_ok=True)

    for file_key in range(3):
        index_path = os.path.join(path, "Resources", systems[system][file_key])
        check_and_generate_file(index_path)

    print(f"Looking for files in {roms_path}")

    files = [file for file in os.scandir(roms_path) if check_rom(file)]
    no_files = len(files)

    filenames = [file.name for file in files] if files else []
    stripped_names = [strip_file_extension(name) for name in filenames] if files else []

    name_map_files = dict(zip(filenames, filenames))
    name_map_cn = dict(zip(filenames, stripped_names))
    name_map_pinyin = dict(zip(filenames, stripped_names))

    write_index_file(name_map_files, sort_without_file_ext, os.path.join(path, "Resources", systems[system][0]))
    write_index_file(name_map_cn, sort_normal, os.path.join(path, "Resources", systems[system][1]))
    write_index_file(name_map_pinyin, sort_normal, os.path.join(path, "Resources", systems[system][2]))

    print(f"Game list for {system} updated with {no_files} ROMs.\n")

def check_and_generate_file(file_path):
    if not os.path.exists(file_path):
        print(f"{file_path} not found. Creating a blank file.")
        try:
            with open(file_path, 'wb') as file_handle:
                file_handle.write(b'')
        except (OSError, IOError):
            print(f"! Failed to create file: {file_path}")
            print("  Check the path and Resources directory are writable.")
            raise StopExecution

def write_index_file(name_map, sort_func, index_path):
    sorted_filenames = sorted(name_map.keys())
    names_bytes = b""
    pointers_by_name = {}

    for filename in sorted_filenames:
        display_name = name_map[filename]
        current_pointer = len(names_bytes)
        pointers_by_name[display_name] = current_pointer
        names_bytes += display_name.encode('utf-8') + chr(0).encode('utf-8')

    metadata_bytes = int_to_4_bytes_reverse(len(name_map))

    sorted_display_names = sort_func(name_map.values())
    sorted_pointers = map(lambda name: pointers_by_name[name], sorted_display_names)

    for current_pointer in sorted_pointers:
        metadata_bytes += int_to_4_bytes_reverse(current_pointer)

    new_index_content = metadata_bytes + names_bytes

    print(f"Overwriting {index_path}")
    try:
        with open(index_path, 'wb') as file_handle:
            file_handle.write(new_index_content)
    except (IOError, OSError):
        print("! Failed overwriting file.")
        print("  Check the path and file are writable, and the file is not open in another program.")
        raise StopExecution

def select_folder():
    folder_selected = filedialog.askdirectory(title="Select Folder")
    if folder_selected:
        path_entry.delete(0, tk.END)
        path_entry.insert(0, folder_selected)
        check_and_find_ini()

def show_popup():
    messagebox.showinfo("Message", "Updated games list!")

def run():
    root = tk.Tk()
    app = FrogtoolGUIe(root)
    root.mainloop()

    def execute_conversion():
        path = path_entry.get() if custom_path_var.get() else drive_combobox.get()
        system = system_var.get()

        if not path:
            print("No path has been selected.")
            return

        try:
            if system == "ALL":
                keys_to_process = [key for key in systems.keys() if key != "ALL"]
            else:
                keys_to_process = [system]

            for syskey in keys_to_process:
                process_sys(path, syskey)

            show_popup()

        except StopExecution:
            print("Error updating game list.")

    drive_label = tk.Label(root, text="SF2000 SD Card Location:")
    drive_combobox = ttk.Combobox(root, state="readonly", width=37)
    drive_combobox.bind("<<ComboboxSelected>>", on_drive_selected)  # Evento para manejar selección de unidad

    custom_path_var = tk.BooleanVar()
    custom_path_checkbox = ttk.Checkbutton(root, text="Use Custom Path", variable=custom_path_var)
    path_label = tk.Label(root, text="Custom Path:")
    path_entry = ttk.Entry(root, width=40)
    path_button = ttk.Button(root, text="Browse", command=select_folder)

    system_label = tk.Label(root, text="Select System:")
    system_var = tk.StringVar(root)
    system_var.set("ALL")
    system_menu = tk.OptionMenu(root, system_var, *systems.keys())

    execute_button = tk.Button(root, text="Update Games List", command=execute_conversion)

    drive_label.pack(pady=5)
    drive_combobox.pack(pady=5)
    custom_path_checkbox.pack(pady=5)
    path_label.pack(pady=5)
    path_entry.pack(pady=5)
    path_button.pack(pady=5)
    system_label.pack(pady=5)
    system_menu.pack(pady=5)
    execute_button.pack(pady=10)

    # Inicializar drives después de que la ventana está lista
    root.after(100, browse_drive)

    root.mainloop()

if __name__ == "__main__":
    systems = {
        "FC": ["rdbui.tax", "fhcfg.nec", "nethn.bvs"],
        "SFC":     ["urefs.tax", "adsnt.nec", "xvb6c.bvs"],
        "MD":     ["scksp.tax", "setxa.nec", "wmiui.bvs"],
        "GB":    ["vdsdc.tax", "umboa.nec", "qdvd6.bvs"],
        "GBC":    ["pnpui.tax", "wjere.nec", "mgdel.bvs"],
        "GBA":     ["vfnet.tax", "htuiw.nec", "sppnp.bvs"],
        "ARCADE":    ["mswb7.tax", "msdtc.nec", "mfpmp.bvs"],
        "ALL": []  # Placeholder for "ALL" option
    }
    supported_rom_ext = [
        "bkp", "zip", "zfc", "zsf", "zmd", "zgb", "zfb", "smc", "fig", "sfc", "gd3", "gd7", "dx2", "bsx", "swc", "nes",
        "nfc", "fds", "unf", "gba", "agb", "gbz", "gbc", "gb", "sgb", "bin", "md", "smd", "gen", "sms"
    ]
    run()
