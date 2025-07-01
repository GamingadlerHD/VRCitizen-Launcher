# gui.py
import ctypes
import sys
import tkinter as tk
from tkinter import messagebox
import customtkinter as ctk
from GUI.Components.vorpXsettings import createVorpXFrame
from GUI.Components.info import create_info_frame
from GUI.Components.settings import create_settings_frame
from GUI.Components.home import create_main_window
from i18n import set_language, translate
from config import add_or_change_value_in_config
from constants import SECONDARY_BG_COLOR, MENU_BUTTON_COLOR, MENU_SELECTED_COLOR

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

    menu_bar = ctk.CTkFrame(root, height=40, fg_color=SECONDARY_BG_COLOR)
    menu_bar.pack(fill="x", side="top")

    nav_options = [
        (translate("home"), "home"),
        (translate("setting"), "settings"),
        (translate("vorpxframe"), "vorpx"),
        (translate("info"), "info"),
    ]

    def on_nav_change(choice):
        if choice == "home":
            show_frame(home_frame)
        elif choice == "settings":
            show_frame(settings_frame)
        elif choice == "vorpx":
            show_frame(vorpX_frame)
        elif choice == "info":
            show_frame(info_frame)

    nav_buttons = {}

    def on_nav_click(selected_name):
        for name, btn in nav_buttons.items():
            if name == selected_name:
                btn.configure(fg_color=MENU_SELECTED_COLOR)
            else:
                btn.configure(fg_color=MENU_BUTTON_COLOR)

    for display_name, internal_name in nav_options:
        def make_command(name=internal_name):
            return lambda: [on_nav_change(name), on_nav_click(name)]

        btn = ctk.CTkButton(
            menu_bar,
            text=display_name.title(),
            command=make_command(),
            corner_radius=0,
            fg_color="transparent",
            width=100, height=40,
        )
        btn.pack(side="left", padx=0, pady=0)
        nav_buttons[internal_name] = btn

    # Language Dropdown
    language_var = tk.StringVar(value=translate("Language"))
    language_options = [
        ("English", "en"),
        ("Deutsch", "de"),
        ("Italiano", "it"),
        ("Español", "es"),
        ("русский", "ru"),
        ("français", "fr"),
    ]
    def on_language_change(choice):
        code = dict(language_options)[choice]
        change_language(code, root)

    language_menu = ctk.CTkOptionMenu(
        menu_bar,
        variable=language_var,
        values=[name for name, _ in language_options],
        command=on_language_change
    )
    language_menu.pack(side="right", padx=5, pady=5)


    # --- Pages container ---
    container = ctk.CTkFrame(root)
    container.pack(fill="both", expand=True)

    home_frame, components, buttons = create_main_window(container)
    info_frame = create_info_frame(container)
    settings_frame, settings = create_settings_frame(container)
    vorpX_frame, vorpX_settings = createVorpXFrame(container)

    for frame in (home_frame, vorpX_frame, info_frame, settings_frame):
        frame.grid(row=0, column=0, columnspan=6, rowspan=10, sticky="nsew")

    on_nav_click("home")  # Set default page to home
    on_nav_change("home")

    return components, settings, buttons, vorpX_settings





