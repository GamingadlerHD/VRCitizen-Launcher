import tkinter as tk
from tkinter import ttk  # Required for Combobox
from i18n import translate
from tkinter import filedialog
import json

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



def create_main_window(container):
    frame = tk.Frame(container)
    # Star Citizen Folder
    tk.Label(frame, text=translate("sc_folder")).grid(row=0, column=0, padx=5, pady=5, sticky="w")
    sc_entry = tk.Entry(frame, width=50)
    sc_entry.grid(row=0, column=1, padx=5, pady=5)
    tk.Button(frame, text=translate("Browse"), command=lambda: browse_folder(sc_entry)).grid(row=0, column=2, padx=5, pady=5)

    # VorpX Exe
    tk.Label(frame, text=translate("vorpX_exe")).grid(row=1, column=0, padx=5, pady=5, sticky="w")
    vorpx_entry = tk.Entry(frame, width=50)
    vorpx_entry.grid(row=1, column=1, padx=5, pady=5)
    tk.Button(frame, text=translate("Browse"), command=lambda: browse_file(vorpx_entry, [('Executables', '*.exe')])).grid(row=1, column=2, padx=5, pady=5)

    # Launcher Exe
    tk.Label(frame, text=translate("Launcher_Exe")).grid(row=2, column=0, padx=5, pady=5, sticky="w")
    launcher_entry = tk.Entry(frame, width=50)
    launcher_entry.grid(row=2, column=1, padx=5, pady=5)
    tk.Button(frame, text=translate("Browse"), command=lambda: browse_file(launcher_entry, [('Executables', '*.exe')])).grid(row=2, column=2, padx=5, pady=5)

    # Divider Line
    ttk.Separator(frame, orient="horizontal").grid(row=3, column=0, columnspan=3, sticky="ew", pady=10)

    # Templates Dropdown
    templates = load_templates()
    tk.Label(frame, text=translate("templates")).grid(row=4, column=0, padx=5, pady=5, sticky="w")
    dropdown = ttk.Combobox(frame, values=[translate("no_template")] + [tmpl['name'] for tmpl in templates])
    dropdown.grid(row=4, column=1, columnspan=2, padx=5, pady=5, sticky="ew")
    dropdown.bind("<<ComboboxSelected>>", lambda event: on_dropdown_change(event, dropdown, fov_entry, width_entry, height_entry))
    dropdown.current(0)

    # FOV, Width, Height
    tk.Label(frame, text="FOV").grid(row=5, column=0, padx=5, pady=5, sticky="w")
    fov_entry = tk.Entry(frame, width=10)
    fov_entry.grid(row=5, column=1, padx=5, pady=5, sticky="w")

    tk.Label(frame, text=translate("width")).grid(row=5, column=2, padx=5, pady=5, sticky="w")
    width_entry = tk.Entry(frame, width=10)
    width_entry.grid(row=5, column=3, padx=5, pady=5, sticky="w")

    tk.Label(frame, text=translate("height")).grid(row=5, column=4, padx=5, pady=5, sticky="w")
    height_entry = tk.Entry(frame, width=10)
    height_entry.grid(row=5, column=5, padx=5, pady=5, sticky="w")

    # Divider Line
    ttk.Separator(frame, orient="horizontal").grid(row=6, column=0, columnspan=6, sticky="ew", pady=10)

    # Hook Checkbox
    use_dxgi = tk.IntVar()
    use_dxgi_check = tk.Checkbutton(frame, text=translate("use_dxgi"), variable=use_dxgi)
    use_dxgi_check.grid(row=7, column=0, columnspan=4, padx=5, pady=5, sticky="w")


    # Stay in VR Checkbox
    stay_in_vr = tk.IntVar()
    stay_in_vr_check = tk.Checkbutton(frame, text=translate("revert"), variable=stay_in_vr)
    stay_in_vr_check.grid(row=8, column=0, columnspan=4, padx=5, pady=5, sticky="w")

    # Buttons
    save_button = tk.Button(frame, text=translate("save"))
    save_button.grid(row=9, column=0, padx=5, pady=5)
    launch_button = tk.Button(frame, text=translate("launch"))
    launch_button.grid(row=9, column=1, padx=5, pady=5)
    res_button = tk.Button(frame, text=translate("restore"))
    res_button.grid(row=9, column=2, padx=5, pady=5)

    components = {
        'sc_entry': sc_entry,
        'vorpx_entry': vorpx_entry,
        'save_button': save_button,
        'launch_button': launch_button,
        'res_button': res_button,
        'fov_entry': fov_entry,
        'width_entry': width_entry,
        'height_entry': height_entry,
        'stay_in_vr': stay_in_vr,
        'launcher_entry': launcher_entry
    }

    return frame, components