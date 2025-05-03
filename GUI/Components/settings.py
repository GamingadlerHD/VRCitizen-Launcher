import tkinter as tk
from tkinter import ttk
from typing import List
from i18n import translate

def set_standard_settings(settings :List[dict]):
    # Set default values for the checkboxes
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
    frame = tk.Frame(container)


    
    # Hook Checkbox
    mb = tk.BooleanVar()
    mb_check = tk.Checkbutton(frame, text=translate("MotionBlur"), variable=mb)
    mb_check.grid(row=1, column=0, columnspan=1, padx=5, pady=5, sticky="w")

    vs = tk.BooleanVar()
    vs_check = tk.Checkbutton(frame, text=translate("VSync"), variable=vs)
    vs_check.grid(row=2, column=0, columnspan=1, padx=5, pady=5, sticky="w")

    # AutoZoomOnSelectedTarget Checkbox
    auto_zoom = tk.BooleanVar()
    auto_zoom_check = tk.Checkbutton(frame, text=translate("AutoZoomOnSelectedTarget"), variable=auto_zoom)
    auto_zoom_check.grid(row=3, column=0, columnspan=1, padx=5, pady=5, sticky="w")

    # ChromaticAberration Checkbox
    ca = tk.BooleanVar()
    chromatic_aberration_check = tk.Checkbutton(frame, text=translate("ChromaticAberration"), variable=ca)
    chromatic_aberration_check.grid(row=4, column=0, columnspan=1, padx=5, pady=5, sticky="w")

    # FilmGrain Checkbox
    fg = tk.BooleanVar()
    film_grain_check = tk.Checkbutton(frame, text=translate("FilmGrain"), variable=fg)
    film_grain_check.grid(row=5, column=0, columnspan=1, padx=5, pady=5, sticky="w")

    # SpringMovment Checkbox
    sp = tk.BooleanVar()
    spring_check = tk.Checkbutton(frame, text=translate("SpringMovment"), variable=sp)
    spring_check.grid(row=6, column=0, columnspan=1, padx=5, pady=5, sticky="w")

    headtracking_label = tk.Label(frame, text=translate("Headtracking"))
    headtracking_label.grid(row=0, column=2, padx=5, pady=5, sticky="w")

    # HeadtrackingToggle Checkbox
    headtracking_toggle = tk.BooleanVar()
    headtracking_toggle_check = tk.Checkbutton(frame, text=translate("HeadtrackingToggle"), variable=headtracking_toggle)
    headtracking_toggle_check.grid(row=1, column=2, columnspan=1, padx=5, pady=5, sticky="w")

    # HeadtrackingDisableDuringADS Checkbox
    headtracking_ads = tk.BooleanVar()
    headtracking_ads_check = tk.Checkbutton(frame, text=translate("HeadtrackingDisableDuringADS"), variable=headtracking_ads)
    headtracking_ads_check.grid(row=2, column=2, columnspan=1, padx=5, pady=5, sticky="w")

    # HeadtrackingDisableDuringMobiGlas Checkbox
    headtracking_mobi = tk.BooleanVar()
    headtracking_mobi_check = tk.Checkbutton(frame, text=translate("HeadtrackingDisableDuringMobiGlas"), variable=headtracking_mobi)
    headtracking_mobi_check.grid(row=3, column=2, columnspan=1, padx=5, pady=5, sticky="w")

    # HeadtrackingDisableDuringWalking Checkbox
    headtracking_walk = tk.BooleanVar()
    headtracking_walk_check = tk.Checkbutton(frame, text=translate("HeadtrackingDisableDuringWalking"), variable=headtracking_walk)
    headtracking_walk_check.grid(row=4, column=2, columnspan=1, padx=5, pady=5, sticky="w")

    # HeadtrackingEnableRollFPS Checkbox
    headtracking_roll = tk.BooleanVar()
    headtracking_roll_check = tk.Checkbutton(frame, text=translate("HeadtrackingEnableRollFPS"), variable=headtracking_roll)
    headtracking_roll_check.grid(row=5, column=2, columnspan=1, padx=5, pady=5, sticky="w")

    # HeadtrackingThirdPersonCameraToggle Checkbox
    headtracking_third_person = tk.BooleanVar()
    headtracking_third_person_check = tk.Checkbutton(frame, text=translate("HeadtrackingThirdPersonCameraToggle"), variable=headtracking_third_person)
    headtracking_third_person_check.grid(row=6, column=2, columnspan=1, padx=5, pady=5, sticky="w")

    # HeadtrackingThirdPersonDisableDuringInventory Checkbox
    headtracking_inventory = tk.BooleanVar()
    headtracking_inventory_check = tk.Checkbutton(frame, text=translate("HeadtrackingThirdPersonDisableDuringInventory"), variable=headtracking_inventory)
    headtracking_inventory_check.grid(row=7, column=2, columnspan=1, padx=5, pady=5, sticky="w")

    gforce_label = tk.Label(frame, text=translate("GForceBoostZoomScale"))
    gforce_label.grid(row=1, column=3, padx=5, pady=5, sticky="w")
    gforce_slider = tk.Scale(frame, from_=0, to=100, orient="horizontal", resolution=5)
    gforce_slider.grid(row=1, column=4, padx=5, pady=5, sticky="ew")

    # GForceHeadBobScale Slider
    gforce_headbob_label = tk.Label(frame, text=translate("GForceHeadBobScale"))
    gforce_headbob_label.grid(row=2, column=3, padx=5, pady=5, sticky="w")
    gforce_headbob_slider = tk.Scale(frame, from_=0, to=100, orient="horizontal", resolution=5)
    gforce_headbob_slider.grid(row=2, column=4, padx=5, pady=5, sticky="ew")

    # ShakeScale Slider
    shake_scale_label = tk.Label(frame, text=translate("ShakeScale"))
    shake_scale_label.grid(row=3, column=3, padx=5, pady=5, sticky="w")
    shake_scale_slider = tk.Scale(frame, from_=0, to=100, orient="horizontal", resolution=5)
    shake_scale_slider.grid(row=3, column=4, padx=5, pady=5, sticky="ew")

    max_autozoom_label = tk.Label(frame, text=translate("MaxAutoZoom"))
    max_autozoom_label.grid(row=4, column=3, padx=5, pady=5, sticky="w")
    max_autozoom_slider = tk.Scale(frame, from_=0, to=100, orient="horizontal", resolution=1)
    max_autozoom_slider.grid(row=4, column=4, padx=5, pady=5, sticky="ew")

    # combobox for HeadtrackingSource, with options "Faceware FOIP" and "TrackIR" and "Tobi", should be saved as a int
    # 0 = Faceware FOIP, 1 = TrackIR, 2 = Tobi
    tk.Label(frame, text=translate("HeadtrackingSource")).grid(row=5, column=3, padx=5, pady=5, sticky="w")
    headtracking_source = tk.StringVar()
    headtracking_source_combobox = ttk.Combobox(frame, textvariable=headtracking_source)
    headtracking_source_combobox['values'] = ("Faceware FOIP", "TrackIR", "Tobi")
    headtracking_source_combobox.grid(row=5, column=4, padx=5, pady=5, sticky="ew")




    data = {
        "MotionBlur": mb,
        "VSync": vs,
        "AutoZoomOnSelectedTarget": auto_zoom,
        "ChromaticAberration": ca,
        "FilmGrain": fg,
        "HeadtrackingToggle": headtracking_toggle,
        "HeadtrackingDisableDuringADS": headtracking_ads,
        "HeadtrackingDisableDuringMobiGlas": headtracking_mobi,
        "HeadtrackingDisableDuringWalking": headtracking_walk,
        "HeadtrackingEnableRollFPS": headtracking_roll,
        "HeadtrackingThirdPersonCameraToggle": headtracking_third_person,
        "HeadtrackingThirdPersonDisableDuringInventory": headtracking_inventory,
        "ShakeScale": shake_scale_slider,
        "GForceBoostZoomScale": gforce_slider,
        "MaxAutoZoom": max_autozoom_slider,
        "HeadtrackingSource": headtracking_source,
        "CameraSpringMovement": sp,
        "GForceHeadBobScale": gforce_headbob_slider,

    }

    set_standard_settings(data)

    # reset button
    reset_button = tk.Button(frame, text=translate("reset"), command=lambda: set_standard_settings(data))
    reset_button.grid(row=9, column=3, padx=5, pady=5)

    return frame, data