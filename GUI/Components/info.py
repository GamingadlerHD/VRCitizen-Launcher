import tkinter as tk
import webbrowser
from i18n import translate

def open_url(url):
    webbrowser.open(url)

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
