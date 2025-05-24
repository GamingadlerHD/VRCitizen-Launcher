import webbrowser
import customtkinter as ctk
from PIL import Image
from i18n import translate
from constants import MAIN_BG_COLOR

STYLE_CONFIG = {
    "font_family": "Arial",
    "heading_font": ("Arial", 16, "bold"),
    "body_font": ("Arial", 14),
    "link_font": ("Arial", 14, "underline"),
    "text_color": "#FFFFFF",
    "link_color": "#00B0F0",
    "hover_color": "#008CBA",
    "frame_width": 800,
    "frame_height": 600,
    "logo_size": (150, 150)
}

def open_url(url):
    webbrowser.open(url)

def create_info_frame(container):
    frame = ctk.CTkFrame(container, fg_color=MAIN_BG_COLOR)
    
    # Load and display logos
    try:
        logo1 = ctk.CTkImage(Image.open("media/logo1.png"), 
                           size=STYLE_CONFIG["logo_size"])
        logo2 = ctk.CTkImage(Image.open("media/logo2.png"), 
                           size=STYLE_CONFIG["logo_size"])
        
        logo_left = ctk.CTkLabel(frame, image=logo1, text="")
        logo_right = ctk.CTkLabel(frame, image=logo2, text="")
        logo_left.pack(side="left", padx=20, pady=20)
        logo_right.pack(side="right", padx=20, pady=20)
    except Exception as e:
        print(f"Error loading logos: {e}")

    # Developer section
    ctk.CTkLabel(frame, 
                text=translate("made_by"),
                font=STYLE_CONFIG["heading_font"]).pack(pady=15)
    
    # Donation info
    ctk.CTkLabel(frame, 
                text=translate("donate"),
                font=STYLE_CONFIG["body_font"],
                wraplength=STYLE_CONFIG["frame_width"] - 100).pack(pady=10, padx=20)

    # GitHub link
    github = ctk.CTkLabel(frame, 
                        text=translate("github"),
                        font=STYLE_CONFIG["link_font"],
                        text_color=STYLE_CONFIG["link_color"],
                        cursor="hand2")
    github.pack(pady=10)
    github.bind("<Button-1>", lambda e: open_url("https://github.com/GamingadlerHD"))
    github.bind("<Enter>", lambda e: github.configure(text_color=STYLE_CONFIG["hover_color"]))
    github.bind("<Leave>", lambda e: github.configure(text_color=STYLE_CONFIG["link_color"]))

    # Discord section
    ctk.CTkLabel(frame, 
                text=translate("support"),
                font=STYLE_CONFIG["body_font"]).pack(pady=15)
    
    discord = ctk.CTkLabel(frame, 
                          text=translate("join"),
                          font=STYLE_CONFIG["link_font"],
                          text_color=STYLE_CONFIG["link_color"],
                          cursor="hand2")
    discord.pack(pady=10)
    discord.bind("<Button-1>", lambda e: open_url("https://discord.gg/StarCitizen"))
    discord.bind("<Enter>", lambda e: discord.configure(text_color=STYLE_CONFIG["hover_color"]))
    discord.bind("<Leave>", lambda e: discord.configure(text_color=STYLE_CONFIG["link_color"]))

    # Copyright information
    ctk.CTkLabel(frame, 
                text=translate("copyright"),
                font=("Arial", 12)).pack(side="bottom", pady=10)
    
    license_link = ctk.CTkLabel(frame, 
                               text="http://creativecommons.org/licenses/by-nc-nd/4.0/",
                               font=("Arial", 12),
                               text_color=STYLE_CONFIG["link_color"],
                               cursor="hand2")
    license_link.pack(side="bottom", pady=5)
    license_link.bind("<Button-1>", lambda e: open_url("http://creativecommons.org/licenses/by-nc-nd/4.0/"))
    license_link.bind("<Enter>", lambda e: license_link.configure(text_color=STYLE_CONFIG["hover_color"]))
    license_link.bind("<Leave>", lambda e: license_link.configure(text_color=STYLE_CONFIG["link_color"]))

    return frame