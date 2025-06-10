import os
import tkinter as tk 
from tkinter import filedialog
import webbrowser
import customtkinter as ctk
from i18n import translate
from constants import DXGI_DLL, MAIN_BG_COLOR, SECONDARY_BG_COLOR
from templates import get_templates, GetPresets

# Set CustomTkinter appearance mode
ctk.set_appearance_mode("system")
ctk.set_default_color_theme("blue") 


def open_url(url):
    webbrowser.open(url)

def set_dxgi_toggle(dxgi_toggle, dxgi_label, sc_path):
    print("Check for dxgi.dll")
    localPath = os.getcwd()
    if not (sc_path.get() and os.path.isfile(os.path.join(sc_path.get(), DXGI_DLL))) and not os.path.isfile(os.path.join(localPath, 'dxgi.dll')):
        dxgi_toggle.configure(state=ctk.DISABLED)
        dxgi_label.configure(text=translate("dxgi_info"))
    else:
        dxgi_toggle.configure(state=ctk.NORMAL)
        dxgi_label.configure(text=translate("dxgi_info_enabled"))

def get_fov(template_name):
    templates = get_templates()
    for template in templates:
        if template['name'] == template_name:
            return template['fov']
    return 0

def on_template_selected(selected_template, preset_dropdown, fov_entry):
    presets = [translate("no_preset")]
    
    if selected_template != translate("no_template"):
        template_presets = GetPresets(selected_template)
        template_fov = get_fov(selected_template)
        fill_entry(fov_entry, template_fov)
        presets += [p['name'] for p in template_presets]
    
    preset_dropdown.configure(values=presets)
    preset_dropdown.set(presets[0])

def on_preset_selected(selected_preset, template_dropdown, width_entry, height_entry):
    if selected_preset == translate("no_preset"):
        return
    
    template_name = template_dropdown.get()
    presets = GetPresets(template_name)
    
    for preset in presets:
        if preset['name'] == selected_preset:
            fill_entry(width_entry, preset['width'])
            fill_entry(height_entry, preset['height'])
            break

def fill_entry(entry, value):
    entry.delete(0, "end")
    entry.insert(0, str(value))

def on_wh_change(width_entry, height_entry, is_height_changed, template_dropdown, preset_dropdown):
    template_name = template_dropdown.get()
    if not template_name or template_name == translate("no_template"):
        return
    
    selected_preset = preset_dropdown.get()
    presets = GetPresets(template_name)
    
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
    frame = ctk.CTkFrame(container, fg_color=MAIN_BG_COLOR)
    
    # Configure main columns (60-40 split)
    frame.grid_columnconfigure(0, weight=6)
    frame.grid_columnconfigure(1, weight=4)
    
    # ===== LEFT PANEL CONTENT =====
    # File Paths Section
    paths_frame = ctk.CTkFrame(frame, corner_radius=5, fg_color=SECONDARY_BG_COLOR)
    paths_frame.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
    ctk.CTkLabel(paths_frame, text=translate("file_paths")).pack(pady=5)
    
    def create_path_row(parent, label_text, file_types=None):
        row_frame = ctk.CTkFrame(parent, fg_color=SECONDARY_BG_COLOR)
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
    vorpx_entry = create_path_row(paths_frame, "vorpX_exe", [('Executables', '*.exe')])
    launcher_entry = create_path_row(paths_frame, "Launcher_Exe", [('Executables', '*.exe')])
    
    # Template/Resolution Section
    template_res_frame = ctk.CTkFrame(frame, corner_radius=5, fg_color=SECONDARY_BG_COLOR)
    template_res_frame.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)
    ctk.CTkLabel(template_res_frame, text=translate("template_resolution_settings")).pack(pady=2)

    columns_frame = ctk.CTkFrame(template_res_frame, fg_color=SECONDARY_BG_COLOR)
    columns_frame.pack(fill="x", pady=5)

    # Left column (template and FOV)
    left_column = ctk.CTkFrame(columns_frame, fg_color=SECONDARY_BG_COLOR)
    left_column.pack(side="left", expand=True, fill="x", padx=5)

    #   Template dropdown row
    template_row = ctk.CTkFrame(left_column, fg_color=SECONDARY_BG_COLOR)
    template_row.pack(fill="x", pady=(0, 10))
    ctk.CTkLabel(template_row, text=translate("template"), width=70).pack(side="left", padx=2)
    templates = get_templates()
    template_dropdown = ctk.CTkOptionMenu(
        template_row,
        values=[translate("no_template")] + [tmpl['name'] for tmpl in templates],
        command=lambda v: on_template_selected(v, preset_dropdown, fov_entry)
    )
    template_dropdown.pack(side="left", padx=5, expand=True, fill="x")

    fov_row = ctk.CTkFrame(left_column, fg_color=SECONDARY_BG_COLOR)
    fov_row.pack(fill="x")
    ctk.CTkLabel(fov_row, text="FOV", width=70).pack(side="left", padx=2)
    fov_entry = ctk.CTkEntry(fov_row, width=60)
    fov_entry.pack(side="left", padx=5)
    fov_entry.bind("<KeyRelease>", lambda e: numbers_only(fov_entry))

    # Right column (preset and resolution)
    right_column = ctk.CTkFrame(columns_frame, fg_color=SECONDARY_BG_COLOR)
    right_column.pack(side="right", expand=True, fill="x", padx=5)

    # Preset dropdown row
    preset_row = ctk.CTkFrame(right_column, fg_color=SECONDARY_BG_COLOR)
    preset_row.pack(fill="x", pady=(0, 10))
    ctk.CTkLabel(preset_row, text=translate("preset"), width=70).pack(side="left", padx=2)
    preset_dropdown = ctk.CTkOptionMenu(
        preset_row,
        values=[translate("no_preset")],
        command=lambda v: on_preset_selected(v, template_dropdown, width_entry, height_entry)
    )
    preset_dropdown.pack(side="left", padx=5, expand=True, fill="x")

    res_row = ctk.CTkFrame(right_column, fg_color=SECONDARY_BG_COLOR)
    res_row.pack(fill="x")
    ctk.CTkLabel(res_row, text=translate("resolution"), width=70).pack(side="left", padx=2)
    width_entry = ctk.CTkEntry(res_row, width=60)
    width_entry.pack(side="left", padx=5)
    ctk.CTkLabel(res_row, text="x").pack(side="left", padx=5)
    height_entry = ctk.CTkEntry(res_row, width=60)
    height_entry.pack(side="left", padx=5)
    
    width_entry.bind("<KeyRelease>", 
                    lambda e: on_wh_change(width_entry, height_entry, False, template_dropdown, preset_dropdown))
    height_entry.bind("<KeyRelease>", 
                     lambda e: on_wh_change(width_entry, height_entry, True, template_dropdown, preset_dropdown))
    
    # ===== RIGHT PANEL CONTENT =====
    right_frame = ctk.CTkFrame(frame, corner_radius=5, fg_color=SECONDARY_BG_COLOR)
    right_frame.grid(row=0, column=1, rowspan=1, sticky="nsew", padx=5, pady=5)
    ctk.CTkLabel(right_frame, text=translate("additional_settings")).pack(pady=5)
    
    ign_res_warning = tk.IntVar()
    ctk.CTkCheckBox(right_frame, text=translate("ov_resolution"), variable=ign_res_warning).pack(anchor="w", pady=5)
    
    additional_popup = tk.IntVar()
    ctk.CTkCheckBox(right_frame, text=translate("ad_popup"), variable=additional_popup).pack(anchor="w", pady=5)
    
    stay_in_vr = tk.IntVar()
    ctk.CTkCheckBox(right_frame, text=translate("revert"), variable=stay_in_vr).pack(anchor="w", pady=5)

    # ===== DXGI SETTINGS SECTION =====
    dxgi_frame = ctk.CTkFrame(frame, corner_radius=5, fg_color=SECONDARY_BG_COLOR)
    dxgi_frame.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)
    ctk.CTkLabel(dxgi_frame, text=translate("dxgi_settings")).pack(pady=5)

    use_dxgi = tk.IntVar()
    dxgi_toggle = ctk.CTkCheckBox(dxgi_frame, text=translate("use_dxgi"), variable=use_dxgi)
    dxgi_toggle.pack(anchor="w", pady=5)

    dxgi_label = ctk.CTkLabel(dxgi_frame, text=translate("dxgi_info"))
    dxgi_label.pack(pady=5)

    dxgi_btn_row = ctk.CTkFrame(dxgi_frame, fg_color="transparent")
    dxgi_btn_row.pack(pady=5)

    again_button = ctk.CTkButton(dxgi_btn_row, text=translate("dxgi_check_again"))
    help_button = ctk.CTkButton(dxgi_btn_row, text=translate("dxgi_help"))

    again_button.configure(command=lambda: set_dxgi_toggle(dxgi_toggle, dxgi_label, sc_entry))
    help_button.configure(command=lambda: open_url("https://github.com/GamingadlerHD/VRCitizen-Launcher/wiki/Hook-Helper"))

    again_button.pack(side="left", padx=5)
    help_button.pack(side="left", padx=5)


    # ===== ACTION BUTTONS =====
    btn_frame = ctk.CTkFrame(frame, fg_color=MAIN_BG_COLOR)
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
        'res_button': res_button,
    }
    
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_rowconfigure(1, weight=1)

    set_dxgi_toggle(dxgi_toggle, dxgi_label, sc_entry)  # Initial check for dxgi.dll
    
    return frame, components, buttons