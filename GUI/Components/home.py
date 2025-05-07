import tkinter as tk
from tkinter import ttk  # Required for Combobox
from i18n import translate
from tkinter import filedialog
import json

def update_resolution(widht, heigh, height_changed, template_index, preset_index):
    numbers_only(widht)
    numbers_only(heigh)

    preset = None
    if template_index == 0:
        return
    try:
        template = load_templates()[template_index - 1]
        preset = template['presets'][preset_index]
    except IndexError:
        print("Invalid template or preset index.")
        return
    
    ratio = float(float(preset['width'])/float(preset['height']))

    if height_changed:
        if heigh.get() == "":
            print("height is empty")
            return
        
        num = float(heigh.get())*ratio
        # round to int
        widht.delete(0, tk.END)
        widht.insert(0, int(num))
    else:
        if widht.get() == "":
            print("width is empty")
            return
        heigh.delete(0, tk.END)
        heigh.insert(0, int(float(widht.get())/ratio))

def numbers_only(entry):
    input = entry.get()
    for char in entry.get():
        if not char.isdigit():
            entry.delete(0, tk.END)
            corrected_input = input.replace(char, '')
            entry.insert(0, corrected_input)
            break


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
    
def on_dropdown_change(event, dropdown, preset):
    selected_index = dropdown.current()  # Get the selected index

    if selected_index == 0:  # No template selected
        print("No Template Selected")
        preset["values"] = [translate("no_template")]
        preset.current(0)
        return
    else:
        preset["values"] = [p['name'] for p in get_presets(selected_index)]

def on_preset_change(event, dropdown, fov_entry, width_entry, height_entry, preset):
    selected_index = dropdown.current()  # Get the selected index
    selected_preset = preset.current()  # Get the selected preset index

    if selected_index == 0:  # No template selected
        return
    selected_item = load_templates()[selected_index -1] 
    selected_preset_values = selected_item['presets'][selected_preset]

    print(selected_item)
    fov_entry.delete(0, tk.END)
    fov_entry.insert(0, selected_preset_values['fov'])
    width_entry.delete(0, tk.END)
    width_entry.insert(0, selected_preset_values['width'])
    height_entry.delete(0, tk.END)
    height_entry.insert(0, selected_preset_values['height'])

def get_presets(template_index):
    templates = load_templates()
    if template_index == 0:
        return []
    else:
        return templates[template_index - 1]['presets']

def create_main_window(container):
    frame = tk.Frame(container, padx=10, pady=10)
    
    # Configure main columns (60-40 split)
    frame.columnconfigure(0, weight=6)  # Left side (60%)
    frame.columnconfigure(1, weight=4)  # Right side (40%)
    
    # ===== LEFT PANEL CONTENT =====
    # File Paths Section
    paths_frame = ttk.LabelFrame(frame, text=translate("file_paths"), padding=10)
    paths_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    
    def create_path_row(parent, label_text, entry_var, row, file_types=None):
        ttk.Label(parent, text=translate(label_text)).grid(row=row, column=0, sticky="w", padx=5)
        entry = ttk.Entry(parent, width=35)
        entry.grid(row=row, column=1, padx=5, sticky="ew")
        btn = ttk.Button(parent, text=translate("Browse"), 
                        command=lambda: browse_file(entry, file_types) if file_types 
                        else browse_folder(entry))
        btn.grid(row=row, column=2, padx=5)
        return entry
    
    sc_entry = create_path_row(paths_frame, "sc_folder", None, 0)
    vorpx_entry = create_path_row(paths_frame, "vorpX_exe", None, 1, [('Executables', '*.exe')])
    launcher_entry = create_path_row(paths_frame, "Launcher_Exe", None, 2, [('Executables', '*.exe')])
    
    # Combined Templates/Resolution Section
    template_res_frame = ttk.LabelFrame(frame, text=translate("template_resolution_settings"), padding=10)
    template_res_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
    
    # Template/Preset Selection
    ttk.Label(template_res_frame, text=translate("template")).grid(row=0, column=0, sticky="w")
    templates = load_templates()
    dropdown = ttk.Combobox(template_res_frame, values=[translate("no_template")] + [tmpl['name'] for tmpl in templates])
    dropdown.grid(row=0, column=1, padx=5, sticky="ew")
    dropdown.current(0)
    
    ttk.Label(template_res_frame, text=translate("preset")).grid(row=0, column=2, padx=(20,5), sticky="w")
    prs = get_presets(dropdown.current())
    preset = ttk.Combobox(template_res_frame, values=[translate("no_preset")] + [p['name'] for p in prs])
    preset.grid(row=0, column=3, padx=5, sticky="ew")
    
    # Resolution Inputs
    ttk.Label(template_res_frame, text="FOV").grid(row=1, column=0, padx=5, pady=10, sticky="w")
    fov_entry = ttk.Entry(template_res_frame, width=8)
    fov_entry.grid(row=1, column=1, padx=5, sticky="w")
    fov_entry.bind("<KeyRelease>", lambda e: numbers_only(fov_entry))
    
    ttk.Label(template_res_frame, text=translate("resolution")).grid(row=1, column=2, padx=(20,5), sticky="e")
    width_entry = ttk.Entry(template_res_frame, width=6)
    width_entry.grid(row=1, column=3, padx=(5, 5), sticky="w")
    ttk.Label(template_res_frame, text="x").grid(row=1, column=3, padx=(55, 5), sticky="w")
    height_entry = ttk.Entry(template_res_frame, width=6)
    height_entry.grid(row=1, column=3, padx=(75, 0), sticky="w")
    
    # Event bindings
    preset.bind("<<ComboboxSelected>>", lambda e: on_preset_change(e, dropdown, fov_entry, width_entry, height_entry, preset))
    dropdown.bind("<<ComboboxSelected>>", lambda e: on_dropdown_change(e, dropdown, preset))
    width_entry.bind("<KeyRelease>", lambda e: update_resolution(width_entry, height_entry, False, dropdown.current(), preset.current()))
    height_entry.bind("<KeyRelease>", lambda e: update_resolution(width_entry, height_entry, True, dropdown.current(), preset.current()))
    
    # ===== RIGHT PANEL CONTENT =====
    right_frame = ttk.LabelFrame(frame, text=translate("additional_settings"), padding=10)
    right_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=5, pady=5)
    
    # Add additional components here (example)
    ign_res_warning = tk.BooleanVar()
    ttk.Checkbutton(right_frame, text=translate("ov_resolution"), variable=ign_res_warning).pack(anchor="w", pady=5)
        
    addidional_popup = tk.BooleanVar()
    ttk.Checkbutton(right_frame, text=translate("ad_popup"), variable=addidional_popup).pack(anchor="w", pady=5)
    
    # ===== BOTTOM SECTION =====
    # Checkboxes
    check_frame = ttk.Frame(frame)
    check_frame.grid(row=2, column=0, columnspan=2, pady=10, sticky="w")
    
    use_dxgi = tk.BooleanVar()
    ttk.Checkbutton(check_frame, text=translate("use_dxgi"), variable=use_dxgi).pack(side="left", padx=10)
    
    stay_in_vr = tk.BooleanVar()
    ttk.Checkbutton(check_frame, text=translate("revert"), variable=stay_in_vr).pack(side="left", padx=10)
    
    # Action Buttons
    btn_frame = ttk.Frame(frame)
    btn_frame.grid(row=3, column=0, columnspan=2, sticky="e", pady=10)
    
    save_button = ttk.Button(btn_frame, text=translate("save"))
    save_button.pack(side="left", padx=5)
    
    launch_button = ttk.Button(btn_frame, text=translate("launch"))
    launch_button.pack(side="left", padx=5)
    
    res_button = ttk.Button(btn_frame, text=translate("restore"))
    res_button.pack(side="left", padx=5)
    
    components = {
        'sc_entry': sc_entry,
        'vorpx_entry': vorpx_entry,
        'launcher_entry': launcher_entry,
        'fov_entry': fov_entry,
        'width_entry': width_entry,
        'height_entry': height_entry,
        'stay_in_vr': stay_in_vr,
        'use_dxgi': use_dxgi,
        'template_dropdown': dropdown,
        'preset_dropdown': preset,
        'ign_res_warning': ign_res_warning,
        'addidional_popup': addidional_popup
    }
    
    buttons = {
        'save_button': save_button,
        'launch_button': launch_button,
        'res_button': res_button
    }
    
    # Configure row weights for proper expansion
    frame.rowconfigure(0, weight=1)
    frame.rowconfigure(1, weight=1)
    
    return frame, components, buttons