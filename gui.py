# gui.py
import json
import tkinter as tk
from tkinter import ttk  # Required for Combobox
from tkinter import filedialog
import webbrowser
from i18n import translate

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

    # Stay in VR Checkbox
    stay_in_vr = tk.IntVar()
    stay_in_vr_check = tk.Checkbutton(frame, text=translate("revert"), variable=stay_in_vr)
    stay_in_vr_check.grid(row=7, column=0, columnspan=2, padx=5, pady=5, sticky="w")

    # Buttons
    save_button = tk.Button(frame, text=translate("save"))
    save_button.grid(row=8, column=0, padx=5, pady=5)
    launch_button = tk.Button(frame, text=translate("launch"))
    launch_button.grid(row=8, column=1, padx=5, pady=5)
    res_button = tk.Button(frame, text=translate("restore"))
    res_button.grid(row=8, column=2, padx=5, pady=5)

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


def create_info_frame(container):
    frame = tk.Frame(container)

    # Logos
    logo1 = tk.PhotoImage(file="image.png") 
    logo2 = tk.PhotoImage(file="image.png")
    logo1 = logo1.subsample(logo1.width() // 150, logo1.height() // 150)
    logo2 = logo2.subsample(logo2.width() // 150, logo2.height() // 150)
    tk.Label(frame, image=logo1).pack(side="left", padx=10, pady=10)
    tk.Label(frame, image=logo2).pack(side="right", padx=10, pady=10)

    # Keep references to the images to prevent garbage collection
    frame.logo1 = logo1
    frame.logo2 = logo2


    tk.Label(frame, text=translate("madeby"), font=("Arial", 14, "bold")).pack(pady=10)
    tk.Label(frame, text=translate("donate"), font=("Arial", 12)).pack(pady=5)

    # GitHub Link
    github_link = tk.Label(frame, text=translate("github"), font=("Arial", 12), fg="blue", cursor="hand2")
    github_link.pack(pady=5)
    github_link.bind("<Button-1>", lambda e: open_url("https://github.com/GamingadlerHD"))

    # Support Info
    tk.Label(frame, text=translate("support"), font=("Arial", 12)).pack(pady=10)

    # Discord Invite
    discord_link = tk.Label(frame, text=translate("join"), font=("Arial", 12), fg="blue", cursor="hand2")
    discord_link.pack(pady=5)
    discord_link.bind("<Button-1>", lambda e: open_url("https://discord.gg/StarCitizen"))

    # Display copyright notice
    tk.Label(frame, text="© 2025 Gamingadler", font=("Arial", 10)).pack(pady=5)
    tk.Label(frame, text=translate("coppyright"), font=("Arial", 10), fg="blue", cursor="hand2").pack(pady=5)
    tk.Label(frame, text="http://creativecommons.org/licenses/by-nc-nd/4.0/", font=("Arial", 10), fg="blue", cursor="hand2").pack(pady=5)
    frame.pack_propagate(False)

    return frame

def create_settings_frame(container):
    frame = tk.Frame(container)
    # Add settings widgets here
    tk.Label(frame, text="Settings").pack(pady=10)
    # Example setting
    tk.Checkbutton(frame, text="Enable Feature X").pack(pady=5)

    data = {
        "setting1": True,
        "setting2": False,
        "setting3": 50
    }
    return frame, data

def open_url(url):
    webbrowser.open(url)

def show_frame(frame):
    frame.tkraise()
    

def setup_gui(root):
    root.title(translate("title"))

    # Top-level Menu
    menu_bar = tk.Menu(root)

    # Home Menu
    home_menu = tk.Menu(menu_bar, tearoff=0)
    home_menu.add_command(label=translate("home"), command=lambda: show_frame(home_frame))
    menu_bar.add_cascade(label=translate("home"), menu=home_menu)

    # Info Menu
    setting_menu = tk.Menu(menu_bar, tearoff=0)
    setting_menu.add_command(label=translate("setting"), command=lambda: show_frame(settings_frame))
    menu_bar.add_cascade(label=translate("setting"), menu=setting_menu)

    info_menu = tk.Menu(menu_bar, tearoff=0)
    info_menu.add_command(label=translate("info"), command=lambda: show_frame(info_frame))
    menu_bar.add_cascade(label=translate("info"), menu=info_menu)

    root.config(menu=menu_bar)


    # --- Pages container ---
    container = tk.Frame(root)
    container.pack(fill="both", expand=True)

    home_frame, components = create_main_window(container)
    info_frame = create_info_frame(container)
    settings_frame, settings = create_settings_frame(container)

    for frame in (home_frame, info_frame, settings_frame):
        frame.grid(row=0, column=0, columnspan=6, rowspan=9, sticky="nsew")

    # Show home frame by default
    show_frame(home_frame)

    return components, settings





