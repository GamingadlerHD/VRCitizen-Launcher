import asyncio
import ctypes
import os
import sys
import threading
import customtkinter
from config import save_input_configs, load_input_config
#from utilities import get_path_from_registery
from GUI.gui import setup_gui
from i18n import set_language
from constants import LAUNCHER_DEFAULT, STARCITIZEN_DEFAULT, VORPX_DEFAULT
from utils.sc_utils import Launch, quit_vr_mode
from utilities import is_admin

if __name__ == "__main__":
    if not is_admin():
        params = " ".join([f'"{arg}"' for arg in sys.argv])
        ctypes.windll.shell32.ShellExecuteW(
            None, "runas", sys.executable, params, None, 1)
        sys.exit()

    # Load config
    config = load_input_config()
    try:
        set_language(config['language'])
    except(KeyError, TypeError):
        set_language('en')

    root = customtkinter.CTk()
    root.iconbitmap("media/i.ico")
    gui_components, settings, interaction, vorpXsettings = setup_gui(root)
    
    # Assign button commands
    interaction['save_button'].configure(command=lambda: save_input_configs(
        [gui_components, settings, vorpXsettings]
    ))

    def async_launch():
        threading.Thread(target=asyncio.run, args=(Launch(gui_components, settings, vorpXsettings),)).start()

    interaction['launch_button'].configure(command=async_launch)

    interaction['res_button'].configure(command=lambda: quit_vr_mode(
        "vorpControl.exe",
        os.path.join(gui_components['sc_entry'].get(), "Bin64/dxgi.dll"),
        os.path.join(gui_components['sc_entry'].get(), "user/client/0/Profiles/default/attributes.xml"),
        gui_components['additional_popup'].get(),
        99999
    ))
    
    def set_component_value(components, componentName, configValue):
        if componentName in components:
            try:
                components[componentName].insert(0, configValue)
            except AttributeError:
                components[componentName].set(configValue)

    if config:
        for k, val in config.items():
            entry_name = k.replace("_val", "")
            for component_dict in (gui_components, settings, vorpXsettings):
                set_component_value(component_dict, entry_name, val)


    else:
        if os.path.exists(STARCITIZEN_DEFAULT):
            gui_components['sc_entry'].insert(0, STARCITIZEN_DEFAULT)
        if os.path.exists(VORPX_DEFAULT):
            gui_components['vorpx_entry'].insert(0, VORPX_DEFAULT)
        if os.path.exists(LAUNCHER_DEFAULT):
            gui_components['launcher_entry'].insert(0, LAUNCHER_DEFAULT)



    root.mainloop()
