import tkinter as tk
from i18n import translate

def create_settings_frame(container):
    frame = tk.Frame(container)
    # Add settings widgets here
    tk.Label(frame, text="Settings").pack(pady=10)
    # Example setting
    tk.Checkbutton(frame, text="Enable Feature X").pack(pady=5)

    data = {
    }
    return frame, data