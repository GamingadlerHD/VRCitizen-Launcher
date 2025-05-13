import tkinter as tk
import customtkinter as ctk
from i18n import translate

def set_standard_settings(settings: dict):
    settings['MotionBlur'].set(0)
    settings['VSync'].set(0)
    settings['AutoZoomOnSelectedTarget'].set(0)
    settings['ChromaticAberration'].set(0)
    settings['FilmGrain'].set(0)
    settings['HeadtrackingToggle'].set(1)
    settings['HeadtrackingDisableDuringADS'].set(0)
    settings['HeadtrackingDisableDuringMobiGlas'].set(0)
    settings['HeadtrackingDisableDuringWalking'].set(0)
    settings['HeadtrackingEnableRollFPS'].set(1)
    settings['HeadtrackingThirdPersonCameraToggle'].set(1)
    settings['HeadtrackingThirdPersonDisableDuringInventory'].set(0)
    settings['ShakeScale'].set(0)
    settings['GForceBoostZoomScale'].set(0)
    settings['MaxAutoZoom'].set(0)
    settings['HeadtrackingSource'].set("TrackIR")
    settings['CameraSpringMovement'].set(0)
    settings['GForceHeadBobScale'].set(0)

    return settings

def create_settings_frame(container):
    frame = ctk.CTkFrame(container)
    frame.grid_rowconfigure(0, weight=1)
    frame.grid_columnconfigure(0, weight=1)

    # Main content container
    content_frame = ctk.CTkFrame(frame)
    content_frame.grid(row=0, column=0, sticky="nsew")

    # Configure columns with equal width
    content_frame.columnconfigure(0, weight=1, uniform='cols')
    content_frame.columnconfigure(2, weight=1, uniform='cols')
    content_frame.columnconfigure(4, weight=1, uniform='cols')

    # Create section frames
    left_frame = ctk.CTkFrame(content_frame)
    middle_frame = ctk.CTkFrame(content_frame)
    right_frame = ctk.CTkFrame(content_frame)

    # Grid layout for content
    left_frame.grid(row=0, column=0, sticky="nsew", padx=5)
    middle_frame.grid(row=0, column=2, sticky="nsew", padx=5)
    right_frame.grid(row=0, column=4, sticky="nsew", padx=5)

    # Custom separators
    sep1 = ctk.CTkFrame(content_frame, width=1, fg_color="#c0c0c0")
    sep2 = ctk.CTkFrame(content_frame, width=1, fg_color="#c0c0c0")
    sep1.grid(row=0, column=1, sticky="ns", padx=5, rowspan=3)
    sep2.grid(row=0, column=3, sticky="ns", padx=5, rowspan=3)

    # Left Column - General Settings
    ctk.CTkLabel(left_frame, text=translate("GeneralSettings"), font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", pady=5)
    checkboxes = [
        ("MotionBlur", 1), ("VSync", 2), ("AutoZoomOnSelectedTarget", 3),
        ("FilmGrain", 4), ("SpringMovment", 5)
    ]
    vars_left = {}
    for text, row in checkboxes:
        var = tk.IntVar()
        ctk.CTkCheckBox(left_frame, text=translate(text), variable=var).grid(
            row=row, column=0, sticky="w", padx=5, pady=2)
        vars_left[text] = var

    # Middle Column - Headtracking
    ctk.CTkLabel(middle_frame, text=translate("Headtracking"), font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", pady=5)
    headtracking_checkboxes = [
        ("HeadtrackingToggle", 1), ("HeadtrackingDisableDuringADS", 2),
        ("HeadtrackingDisableDuringMobiGlas", 3), ("HeadtrackingDisableDuringWalking", 4),
        ("HeadtrackingEnableRollFPS", 5), ("HeadtrackingThirdPersonCameraToggle", 6),
        ("HeadtrackingThirdPersonDisableDuringInventory", 7)
    ]
    vars_middle = {}
    for text, row in headtracking_checkboxes:
        var = tk.IntVar()
        ctk.CTkCheckBox(middle_frame, text=translate(text), variable=var).grid(
            row=row, column=0, sticky="w", padx=5, pady=2)
        vars_middle[text] = var

    # Right Column - Advanced Settings
    ctk.CTkLabel(right_frame, text=translate("AdvancedSettings"), font=ctk.CTkFont(weight="bold")).grid(row=0, column=0, sticky="w", pady=5)
    right_frame.columnconfigure(1, weight=1)
    
    slider_widgets = [
        ("GForceBoostZoomScale", 1), ("GForceHeadBobScale", 2),
        ("ShakeScale", 3), ("MaxAutoZoom", 4), ("ChromaticAberration", 5)
    ]
    vars_right = {}
    for text, row in slider_widgets:
        ctk.CTkLabel(right_frame, text=translate(text)).grid(row=row, column=0, sticky="w", padx=5)
        var = tk.IntVar()
        slider = ctk.CTkSlider(right_frame, from_=0, to=100, variable=var, 
                             orientation="horizontal", number_of_steps=20)
        slider.grid(row=row, column=1, sticky="ew", padx=5)
        vars_right[text] = var

    # Headtracking Source Combobox
    ctk.CTkLabel(right_frame, text=translate("HeadtrackingSource")).grid(row=6, column=0, sticky="w", padx=5)
    headtracking_source = tk.StringVar()
    ctk.CTkComboBox(right_frame, variable=headtracking_source, 
                  values=["Faceware FOIP", "TrackIR", "Tobi"]).grid(
                      row=6, column=1, sticky="ew", padx=5)
    vars_right["HeadtrackingSource"] = headtracking_source

    # Reset Button
    reset_button = ctk.CTkButton(frame, text=translate("reset"))
    reset_button.grid(row=1, column=0, pady=15, sticky="")

    # Combine settings data
    data = {
        **vars_left,
        **vars_middle,
        **vars_right,
        "CameraSpringMovement": vars_left["SpringMovment"]
    }
    set_standard_settings(data)
    reset_button.configure(command=lambda: set_standard_settings(data))

    return frame, data