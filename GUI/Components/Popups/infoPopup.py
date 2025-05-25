import customtkinter as ctk

class InfoPopup(ctk.CTkToplevel):
    def __init__(self, parent, title="Info", message="Information message"):
        super().__init__(parent)
        self.title(title)
        self.geometry("300x150")
        self.resizable(False, False)
        self.grab_set()  # Modal behavior

        label = ctk.CTkLabel(self, text=message, wraplength=280)
        label.pack(pady=20)

        button = ctk.CTkButton(self, text="OK", command=self.destroy)
        button.pack(pady=10)
