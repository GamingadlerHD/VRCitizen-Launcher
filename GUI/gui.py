# gui.py
import tkinter as tk
from i18n import translate
from GUI.Components.info import create_info_frame
from GUI.Components.settings import create_settings_frame
from GUI.Components.home import create_main_window

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

    home_frame, components, buttons = create_main_window(container)
    info_frame = create_info_frame(container)
    settings_frame, settings = create_settings_frame(container)

    for frame in (home_frame, info_frame, settings_frame):
        frame.grid(row=0, column=0, columnspan=6, rowspan=10, sticky="nsew")

    # Show home frame by default
    show_frame(home_frame)

    return components, settings, buttons





