# gui.py
import tkinter as tk
from tkinter import filedialog

def browse_file(entry, filetypes):
    filename = filedialog.askopenfilename(filetypes=filetypes)
    if filename:
        entry.delete(0, tk.END)
        entry.insert(0, filename)

def browse_folder(entry):
    foldername = filedialog.askdirectory()
    if foldername:
        entry.delete(0, tk.END)
        entry.insert(0, foldername)

def setup_gui(root):
    root.title("Star Citizen VR Launcher")

    # Star Citizen Folder
    tk.Label(root, text="Star Citizen Folder").grid(row=0, column=0)
    sc_entry = tk.Entry(root, width=50)
    sc_entry.grid(row=0, column=1)
    tk.Button(root, text="Browse", command=lambda: browse_folder(sc_entry)).grid(row=0, column=2)

    # VorpX Exe
    tk.Label(root, text="vorpX Exe").grid(row=1, column=0)
    vorpx_entry = tk.Entry(root, width=50)
    vorpx_entry.grid(row=1, column=1)
    tk.Button(root, text="Browse", command=lambda: browse_file(vorpx_entry, [('Executables', '*.exe')])).grid(row=1, column=2)

    # EasyAntiCheat Folder
    tk.Label(root, text="EasyAntiCheat Folder").grid(row=2, column=0)
    eac_folder_entry = tk.Entry(root, width=50)
    eac_folder_entry.grid(row=2, column=1)
    tk.Button(root, text="Browse", command=lambda: browse_folder(eac_folder_entry)).grid(row=2, column=2)

    # Original Attributes File
    tk.Label(root, text="Original Attributes File").grid(row=3, column=0)
    attr_orig_entry = tk.Entry(root, width=50)
    attr_orig_entry.grid(row=3, column=1)
    tk.Button(root, text="Browse", command=lambda: browse_file(attr_orig_entry, [('XML Files', '*.xml')])).grid(row=3, column=2)

    # Buttons
    save_button = tk.Button(root, text="Save Config")
    save_button.grid(row=5, column=0)
    launch_button = tk.Button(root, text="Launch")
    launch_button.grid(row=5, column=1)

    return {
        'sc_entry': sc_entry,
        'vorpx_entry': vorpx_entry,
        'eac_folder_entry': eac_folder_entry,
        'attr_orig_entry': attr_orig_entry,
        'save_button': save_button,
        'launch_button': launch_button,
        'root': root
    }