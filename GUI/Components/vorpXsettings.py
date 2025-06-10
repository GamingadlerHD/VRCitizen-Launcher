import customtkinter as ctk
from constants import MAIN_BG_COLOR
from i18n import translate

def createVorpXFrame(container):
    frame = ctk.CTkFrame(container, fg_color=MAIN_BG_COLOR)

    # Configure grid to split frame in half
    frame.columnconfigure(0, weight=1)
    frame.columnconfigure(1, weight=1)

    vr_label = ctk.CTkLabel(frame, text=translate('vorpxlefttitle'), font=ctk.CTkFont(weight="bold"))
    vr_label.grid(row=0, column=0, sticky="w", padx=20, pady=20)

    vorpx_label = ctk.CTkLabel(frame, text=translate('vorpxrighttitle'), font=ctk.CTkFont(weight="bold"))
    vorpx_label.grid(row=0, column=1, sticky="w", padx=20, pady=(20, 5))

    keep_keybinds_var = ctk.BooleanVar()
    keep_keybinds_check = ctk.CTkCheckBox(
        frame, text=translate('keepkeybinds'), variable=keep_keybinds_var
    )
    keep_keybinds_check.grid(row=1, column=1, sticky="w", padx=20, pady=(0, 20))

    data = {
        "keep_keybinds": keep_keybinds_var
        }

    return frame, data