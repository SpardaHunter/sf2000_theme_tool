import os
import re
import binascii
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import psutil

class StopExecution(Exception):
    pass

drive_combobox = None
path_entry = None
system_var = None
system_menu = None
custom_path_var = None

def browse_drive():
    global drive_combobox
    if not drive_combobox:
        return

    drives = [drive.device for drive in psutil.disk_partitions()] if os.name == "nt" else [drive.mountpoint for drive in psutil.disk_partitions()]
    drive_combobox['values'] = drives
    if drives:
        drive_combobox.set(drives[0])

def on_drive_selected(event):
    global custom_path_var, systems, system_var, system_menu
    # Reiniciar systems antes de buscar el nuevo FoldernamX.ini
    systems = {
        "FC": ["m01.ta", "m01.ne", "m01.bv"],
        "SFC": ["m02.ta", "m02.ne", "m02.bv"],
        "MD": ["m03.ta", "m03.ne", "m03.bv"],
        "GB": ["m04.ta", "m04.ne", "m04.bv"],
        "GBC": ["m05.ta", "m05.ne", "m05.bv"],
        "GBA": ["m06.ta", "m06.ne", "m06.bv"],
        "ARCADE": ["m07.ta", "m07.ne", "m07.bv"],
        "SEGA": ["m08.ta", "m08.ne", "m08.bv"],
        "ATARI_NGP": ["m09.ta", "m09.ne", "m09.bv"],
        "WONDERSWAN": ["m10.ta", "m10.ne", "m10.bv"],
        "PCE": ["m11.ta", "m11.ne", "m11.bv"],
        "MULTICORE": ["m12.ta", "m12.ne", "m12.bv"],
        "ALL": []  # Placeholder for "ALL" option
    }
    
    if not custom_path_var.get():  # Solo busca automáticamente si el checkbox está desactivado
        check_and_find_ini()

def int_to_4_bytes_reverse(src_int):
    hex_string = format(src_int, "x").rjust(8, "0")[0:8]
    return binascii.unhexlify(hex_string)[::-1]

def find_foldernamx_ini(path):
    global systems, system_var, system_menu
    ini_path = os.path.join(path, "Resources", "FoldernamX.ini")
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

        updated_systems = dict(zip(new_keys, systems.values()))
        systems = updated_systems

        systems["ALL"] = []

        menu = system_menu["menu"]
        menu.delete(0, "end")
        for key in systems.keys():
            menu.add_command(label=key, command=tk._setit(system_var, key))

        system_var.set("ALL")
        messagebox.showinfo("Success", "Systems updated successfully from FoldernamX.ini!")
        print("Updated systems:", systems)

    except Exception as e:
        messagebox.showerror("Error", f"Failed to read or process {ini_path}: {e}")

def check_and_find_ini():
    global custom_path_var, path_entry, drive_combobox, systems
    if custom_path_var.get():
        path = path_entry.get()
        if path:
            find_foldernamx_ini(path)
    else:
        path = drive_combobox.get()
        if path:
            find_foldernamx_ini(path)

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
    global drive_combobox, path_entry, custom_path_var, system_var, system_menu
    root = tk.Tk()
    root.title("Frogtool GUI")

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
        "FC": ["m01.ta", "m01.ne", "m01.bv"],
        "SFC":     ["m02.ta", "m02.ne", "m02.bv"],
        "MD":     ["m03.ta", "m03.ne", "m03.bv"],
        "GB":    ["m04.ta", "m04.ne", "m04.bv"],
        "GBC":    ["m05.ta", "m05.ne", "m05.bv"],
        "GBA":     ["m06.ta", "m06.ne", "m06.bv"],
        "ARCADE":    ["m07.ta", "m07.ne", "m07.bv"],
        "SEGA":     ["m08.ta", "m08.ne", "m08.bv"],
        "ATARI_NGP":     ["m09.ta", "m09.ne", "m09.bv"],
        "WONDERSWAN":     ["m10.ta", "m10.ne", "m10.bv"],
        "PCE":     ["m11.ta", "m11.ne", "m11.bv"],
        "MULTICORE":     ["m12.ta", "m12.ne", "m12.bv"],
        "ALL": []  # Placeholder for "ALL" option
    }
    supported_rom_ext = [
        "bkp", "zip", "zfc", "zsf", "zmd", "zgb", "zfb", "smc", "fig", "sfc", "gd3", "gd7", "dx2", "bsx", "swc", "nes",
        "nfc", "fds", "unf", "gba", "agb", "gbz", "gbc", "gb", "sgb", "bin", "md", "smd", "gen", "sms"
    ]
    run()
