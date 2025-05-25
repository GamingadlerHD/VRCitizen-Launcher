import customtkinter as ctk

class ConfirmPopup(ctk.CTkToplevel):
    def __init__(self, parent, title="Confirm", message="Are you sure?", on_confirm=None):
        super().__init__(parent)
        self.title(title)
        self.geometry("300x160")
        self.resizable(False, False)
        self.grab_set()

        self.on_confirm = on_confirm

        label = ctk.CTkLabel(self, text=message, wraplength=280)
        label.pack(pady=20)

        button_frame = ctk.CTkFrame(self)
        button_frame.pack(pady=10)

        yes_button = ctk.CTkButton(button_frame, text="Yes", command=self.confirm)
        yes_button.pack(side="left", padx=10)

        no_button = ctk.CTkButton(button_frame, text="No", command=self.destroy)
        no_button.pack(side="left", padx=10)

    def confirm(self):
        if self.on_confirm:
            self.on_confirm()
        self.destroy()
