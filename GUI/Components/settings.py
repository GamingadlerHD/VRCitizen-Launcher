import tkinter as tk
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
        "HeadtrackingThirdPersonDisableDuringInventory": headtracking_inventory

    }

    set_standard_settings(data)

    return frame, data