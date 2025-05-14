import tkinter as tk  # For IntVar, StringVar etc.
from tkinter import filedialog
import json
import customtkinter as ctk
from i18n import translate

# Set CustomTkinter appearance mode
ctk.set_appearance_mode("System")
ctk.set_default_color_theme("blue") 

def get_templates():
    try:
        with open('templates.json', 'r', encoding='utf-8') as f:
            templates = json.load(f)['templates']
        return templates
    except FileNotFoundError:
        return []

def get_presets(template_name):
    templates = get_templates()
    for template in templates:
        if template['name'] == template_name:
            return template['presets']
    return []

def on_template_selected(selected_template, preset_dropdown):
    presets = [translate("no_preset")]
    
    if selected_template != translate("no_template"):
        template_presets = get_presets(selected_template)
        presets += [p['name'] for p in template_presets]
    
    preset_dropdown.configure(values=presets)
    preset_dropdown.set(presets[0])

def on_preset_selected(selected_preset, template_dropdown, fov_entry, width_entry, height_entry):
    if selected_preset == translate("no_preset"):
        return
    
    template_name = template_dropdown.get()
    presets = get_presets(template_name)
    
    for preset in presets:
        if preset['name'] == selected_preset:
            fov_entry.delete(0, "end")
            fov_entry.insert(0, preset['fov'])
            
            width_entry.delete(0, "end")
            width_entry.insert(0, preset['width'])
            
            height_entry.delete(0, "end")
            height_entry.insert(0, preset['height'])
            break

def on_wh_change(width_entry, height_entry, is_height_changed, template_dropdown, preset_dropdown):
    template_name = template_dropdown.get()
    if not template_name or template_name == translate("no_template"):
        return
    
    selected_preset = preset_dropdown.get()
    presets = get_presets(template_name)
    
    preset = None
    for p in presets:
        if p['name'] == selected_preset:
            preset = p
            break
    
    if not preset:
        return
    
    ratio = float(preset['width']) / float(preset['height'])
    
    if is_height_changed:
        if not height_entry.get():
            return
        try:
            num = float(height_entry.get()) * ratio
            width_entry.delete(0, "end")
            width_entry.insert(0, str(int(num)))
        except ValueError:
            pass
    else:
        if not width_entry.get():
            return
        try:
            num = float(width_entry.get()) / ratio
            height_entry.delete(0, "end")
            height_entry.insert(0, str(int(num)))
        except ValueError:
            pass

def numbers_only(entry):
    user_input = entry.get()
    if not user_input.isdigit():
        entry.delete(0, "end")
        entry.insert(0, ''.join(filter(str.isdigit, user_input)))

def browse_file(entry, filetypes):
    filename = filedialog.askopenfilename(filetypes=filetypes)
    if filename:
        entry.delete(0, "end")
        entry.insert(0, filename)

def browse_folder(entry):
    foldername = filedialog.askdirectory()
    if foldername:
        entry.delete(0, "end")
        entry.insert(0, foldername)

def create_main_window(container):
    frame = ctk.CTkFrame(container)
    
    # Configure main columns (60-40 split)
    frame.grid_columnconfigure(0, weight=6)
    frame.grid_columnconfigure(1, weight=4)
    
    # ===== LEFT PANEL CONTENT =====
    # File Paths Section
    paths_frame = ctk.CTkFrame(frame, corner_radius=5)
    paths_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    ctk.CTkLabel(paths_frame, text=translate("file_paths")).pack(pady=5)
    
    def create_path_row(parent, label_text, row, file_types=None):
        row_frame = ctk.CTkFrame(parent)
        row_frame.pack(fill="x", pady=2)
    
        # Configure grid layout for consistent widths
        row_frame.grid_columnconfigure(1, weight=1)
    
        ctk.CTkLabel(row_frame, text=translate(label_text), width=150, anchor='w').grid(row=0, column=0, padx=5, sticky="w")
        entry = ctk.CTkEntry(row_frame)
        entry.grid(row=0, column=1, padx=5, sticky="ew")  # Uniform width
        btn = ctk.CTkButton(row_frame, text=translate("Browse"), width=80,
                       command=lambda: browse_file(entry, file_types) if file_types 
                       else browse_folder(entry))
        btn.grid(row=0, column=2, padx=5)
        return entry
    
    sc_entry = create_path_row(paths_frame, "sc_folder", 0)
    vorpx_entry = create_path_row(paths_frame, "vorpX_exe", 1, [('Executables', '*.exe')])
    launcher_entry = create_path_row(paths_frame, "Launcher_Exe", 2, [('Executables', '*.exe')])
    
    # Template/Resolution Section
    template_res_frame = ctk.CTkFrame(frame, corner_radius=5)
    template_res_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
    ctk.CTkLabel(template_res_frame, text=translate("template_resolution_settings")).pack(pady=5)
    
    # Template/Preset Selection
    template_preset_frame = ctk.CTkFrame(template_res_frame)
    template_preset_frame.pack(fill="x", pady=5)
    
    ctk.CTkLabel(template_preset_frame, text=translate("template")).pack(side="left", padx=5)
    templates = get_templates()
    template_dropdown = ctk.CTkComboBox(
        template_preset_frame,
        values=[translate("no_template")] + [tmpl['name'] for tmpl in templates],
        command=lambda v: on_template_selected(v, preset_dropdown)
    )
    template_dropdown.pack(side="left", padx=5, expand=True, fill="x")
    
    ctk.CTkLabel(template_preset_frame, text=translate("preset")).pack(side="left", padx=20)
    preset_dropdown = ctk.CTkComboBox(
        template_preset_frame,
        values=[translate("no_preset")],
        command=lambda v: on_preset_selected(v, template_dropdown, fov_entry, width_entry, height_entry)
    )
    preset_dropdown.pack(side="left", padx=5, expand=True, fill="x")
    
    # Resolution Inputs
    res_frame = ctk.CTkFrame(template_res_frame)
    res_frame.pack(fill="x", pady=5)
    
    ctk.CTkLabel(res_frame, text="FOV").pack(side="left", padx=5)
    fov_entry = ctk.CTkEntry(res_frame, width=60)
    fov_entry.pack(side="left", padx=5)
    fov_entry.bind("<KeyRelease>", lambda e: numbers_only(fov_entry))
    
    ctk.CTkLabel(res_frame, text=translate("resolution")).pack(side="left", padx=20)
    width_entry = ctk.CTkEntry(res_frame, width=60)
    width_entry.pack(side="left", padx=5)
    ctk.CTkLabel(res_frame, text="x").pack(side="left", padx=5)
    height_entry = ctk.CTkEntry(res_frame, width=60)
    height_entry.pack(side="left", padx=5)
    
    width_entry.bind("<KeyRelease>", 
                    lambda e: on_wh_change(width_entry, height_entry, False, template_dropdown, preset_dropdown))
    height_entry.bind("<KeyRelease>", 
                     lambda e: on_wh_change(width_entry, height_entry, True, template_dropdown, preset_dropdown))
    
    # ===== RIGHT PANEL CONTENT =====
    right_frame = ctk.CTkFrame(frame, corner_radius=5)
    right_frame.grid(row=0, column=1, rowspan=2, sticky="nsew", padx=5, pady=5)
    ctk.CTkLabel(right_frame, text=translate("additional_settings")).pack(pady=5)
    
    # Checkboxes moved to additional settings
    ign_res_warning = tk.IntVar()
    ctk.CTkCheckBox(right_frame, text=translate("ov_resolution"), variable=ign_res_warning).pack(anchor="w", pady=5)
    
    additional_popup = tk.IntVar()
    ctk.CTkCheckBox(right_frame, text=translate("ad_popup"), variable=additional_popup).pack(anchor="w", pady=5)
    
    use_dxgi = tk.IntVar()
    ctk.CTkCheckBox(right_frame, text=translate("use_dxgi"), variable=use_dxgi).pack(anchor="w", pady=5)
    
    stay_in_vr = tk.IntVar()
    ctk.CTkCheckBox(right_frame, text=translate("revert"), variable=stay_in_vr).pack(anchor="w", pady=5)
    
    # ===== ACTION BUTTONS =====
    btn_frame = ctk.CTkFrame(frame)
    btn_frame.grid(row=3, column=0, columnspan=2, sticky="e", pady=10)
    
    save_button = ctk.CTkButton(btn_frame, text=translate("save"), width=80)
    save_button.pack(side="left", padx=5)
    
    launch_button = ctk.CTkButton(btn_frame, text=translate("launch"), width=80)
    launch_button.pack(side="left", padx=5)
    
    res_button = ctk.CTkButton(btn_frame, text=translate("restore"), width=80)
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
        'template_dropdown': template_dropdown,
        'preset_dropdown': preset_dropdown,
        'ign_res_warning': ign_res_warning,
        'additional_popup': additional_popup
    }
    
    buttons = {
        'save_button': save_button,
        'launch_button': launch_button,
        'res_button': res_button
    }
    
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=1)
    
    return frame, components, buttons