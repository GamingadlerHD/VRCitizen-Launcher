# gui.py
import json
import tkinter as tk
from tkinter import ttk  # Required for Combobox
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

#load templates from templates.json
def load_templates():
    try:
        with open('templates.json', 'r') as f:
            templates = json.load(f)['templates']
        return templates
    except FileNotFoundError:
        return {}
    
def on_dropdown_change(event, dropdown, fov_entry, width_entry, height_entry):
    selected_index = dropdown.current()  # Get the selected index
    if selected_index == 0:  # No template selected
        print("No Template Selected")
        return
    else:
        selected_item = load_templates()[selected_index -1]  # Get the corresponding object
        print(f"Selected: {selected_item['name']}")
        # Update the FOV, Width, and Height entries with the selected template values
        fov_entry.delete(0, tk.END)
        fov_entry.insert(0, selected_item['fov'])
        width_entry.delete(0, tk.END)
        width_entry.insert(0, selected_item['width'])
        height_entry.delete(0, tk.END)
        height_entry.insert(0, selected_item['height'])



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

    tk.Label(root, text="Launcher Exe").grid(row=2, column=0)
    launcher_entry = tk.Entry(root, width=50)
    launcher_entry.grid(row=2, column=1)
    tk.Button(root, text="Browse", command=lambda: browse_file(launcher_entry, [('Executables', '*.exe')])).grid(row=2, column=2)

    templates = load_templates()
    dropdown = ttk.Combobox(root, values=["No Template"] + [tmpl['name'] for tmpl in templates])
    dropdown.grid(row=3, column=0, columnspan=2)  # Adjusted to span two columns

    dropdown.bind("<<ComboboxSelected>>", lambda event: on_dropdown_change(event, dropdown, fov_entry, width_entry, height_entry))

    dropdown.current(0)  # Selects the first item initially

    tk.Label(root, text="FOV").grid(row=4, column=0)
    fov_entry = tk.Entry(root, width=10)
    fov_entry.grid(row=4, column=1)

    tk.Label(root, text="Width").grid(row=4, column=2)
    width_entry = tk.Entry(root, width=10)
    width_entry.grid(row=4, column=3)

    tk.Label(root, text="Height").grid(row=4, column=4)
    height_entry = tk.Entry(root, width=10)
    height_entry.grid(row=4, column=5)

    # stay in vr checkbox
    stay_in_vr = tk.IntVar()
    stay_in_vr_check = tk.Checkbutton(root, text="Stay in VR", variable=stay_in_vr)
    stay_in_vr_check.grid(row=5, column=0, columnspan=2)


    # Buttons
    save_button = tk.Button(root, text="Save Config")
    save_button.grid(row=6, column=0)
    launch_button = tk.Button(root, text="Launch")
    launch_button.grid(row=6, column=1)
    res_button = tk.Button(root, text="Restore")
    res_button.grid(row=6, column=2)

    return {
        'sc_entry': sc_entry,
        'vorpx_entry': vorpx_entry,
        'save_button': save_button,
        'launch_button': launch_button,
        'res_button': res_button,
        'fov_entry': fov_entry,
        'width_entry': width_entry,
        'height_entry': height_entry,
        'stay_in_vr': stay_in_vr,
        'launcher_entry': launcher_entry,
        'root': root
    }