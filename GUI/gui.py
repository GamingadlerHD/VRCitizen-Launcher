# gui.py
import ctypes
import sys
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from i18n import set_language, translate
from GUI.Components.info import create_info_frame
from GUI.Components.settings import create_settings_frame
from GUI.Components.home import create_main_window
from config import add_or_change_value_in_config

def show_frame(frame):
    frame.tkraise()

def change_language(language :str, root):

    if messagebox.askyesno(translate("info", language), translate("change_language", language)):
        # Change the language 
        set_language(language)
        # clear root
        for widget in root.winfo_children():
            widget.destroy()
        # Update the GUI with the new language
        add_or_change_value_in_config("language", language)
        params = " ".join([f'"{arg}"' for arg in sys.argv])
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, params, None, 1)
        sys.exit()

    

def setup_gui(root):
    root.title(translate("title"))

    # Top-level Menu
    menu_bar = tk.Menu(root)

    # Home Menu
    home_menu = tk.Menu(menu_bar, tearoff=0)
    home_menu.add_command(label=translate("home"), command=lambda: show_frame(home_frame))
    home_menu.add_command(label=translate("setting"), command=lambda: show_frame(settings_frame))



    menu_bar.add_cascade(label=translate("launcher"), menu=home_menu)

    language_menu = tk.Menu(menu_bar, tearoff=0)
    language_menu.add_command(label="English", command=lambda: change_language("en", root))
    language_menu.add_command(label="Deutsch", command=lambda: change_language("de", root))
    language_menu.add_command(label="Italiano", command=lambda: change_language("it", root))
    language_menu.add_command(label="Español", command=lambda: change_language("es", root))
    language_menu.add_command(label="русский", command=lambda: change_language("ru", root))
    menu_bar.add_cascade(label=translate("Language"), menu=language_menu)

    info_menu = tk.Menu(menu_bar, tearoff=0)
    info_menu.add_command(label=translate("info"), command=lambda: show_frame(info_frame))
    menu_bar.add_cascade(label=translate("info"), menu=info_menu)

    root.config(menu=menu_bar)


    # --- Pages container ---
    container = ctk.CTkFrame(root)
    container.pack(fill="both", expand=True)

    home_frame, components, buttons = create_main_window(container)
    info_frame = create_info_frame(container)
    settings_frame, settings = create_settings_frame(container)

    for frame in (home_frame, info_frame, settings_frame):
        frame.grid(row=0, column=0, columnspan=6, rowspan=10, sticky="nsew")

    # Show home frame by default
    show_frame(home_frame)

    return components, settings, buttons





