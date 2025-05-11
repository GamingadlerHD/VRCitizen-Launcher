import tkinter as tk
from tkinter import ttk  # Required for Combobox
from i18n import translate
from tkinter import filedialog
import json

def get_templates():
    try:
        with open('templates.json', 'r', encoding='utf-8') as f:
            templates = json.load(f)['templates']
        return templates
    except FileNotFoundError:
        return {}
    
def get_presets(template_name):
    templates = get_templates()
    for template in templates:
        if template['name'] == template_name:
            return template['presets']
    return []

def on_template_selected(e, dropdown, preset):
    presets :list[str] = [translate("no_preset")]

    if dropdown.current() != 0:
        template_presets = get_presets(dropdown.get())
        presets.append([p['name'] for p in template_presets])

    preset["values"] = presets
    preset.current(0)

def on_preset_selected(e, preset, template, fov_entry, width_entry, height_entry):
    if preset.current() == 0:
        return
    
    preset_values = get_presets(template.get())[preset.current() - 1]

    fov_entry.delete(0, tk.END)
    fov_entry.insert(0, preset_values['fov'])

    width_entry.delete(0, tk.END)
    width_entry.insert(0, preset_values['width'])

    height_entry.delete(0, tk.END)
    height_entry.insert(0, preset_values['height'])

def on_wh_change(e, width_entry, height_entry, is_height_changed, template, preset):
    template = get_presets(template.get())
    # get preset by name to avoid index issues
    for ps in template:
        if ps['name'] == preset.get():
            preset = ps
            break
    
    ratio = float(float(preset['width'])/float(preset['height']))

    if is_height_changed:
        if height_entry.get() == "":
            print("height is empty")
            return
        
        num = float(height_entry.get())*ratio
        # round to int
        width_entry.delete(0, tk.END)
        width_entry.insert(0, int(num))
    else:
        if width_entry.get() == "":
            print("width is empty")
            return
        num = float(width_entry.get())/ratio
        height_entry.delete(0, tk.END)
        height_entry.insert(0, int(num))
    



# ====== GENERAL FUNCTIONS ======

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
    templates = get_templates()
    dropdown = ttk.Combobox(template_res_frame, values=[translate("no_template")] + [tmpl['name'] for tmpl in templates])
    dropdown.grid(row=0, column=1, padx=5, sticky="ew")
    
    ttk.Label(template_res_frame, text=translate("preset")).grid(row=0, column=2, padx=(20,5), sticky="w")
    prs = get_presets(dropdown.get())
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
    preset.bind("<<ComboboxSelected>>", lambda e: on_preset_selected(e, preset, dropdown, fov_entry, width_entry, height_entry))
    dropdown.bind("<<ComboboxSelected>>", lambda e: on_template_selected(e, dropdown, preset))
    width_entry.bind("<KeyRelease>", lambda e: on_wh_change(e, width_entry, height_entry, False, dropdown, preset))
    height_entry.bind("<KeyRelease>", lambda e: on_wh_change(e, width_entry, height_entry, True, dropdown, preset))
    
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