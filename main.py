import asyncio
import os
import threading
import customtkinter
from config import save_input_configs, load_input_config
#from utilities import get_path_from_registery
from GUI.gui import setup_gui
from i18n import set_language
from constants import LAUNCHER_DEFAULT, STARCITIZEN_DEFAULT, VORPX_DEFAULT
from sc_utils import launch, quit_vr_mode

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
    gui_components, settings, interaction = setup_gui(root)
    
    # Assign button commands
    interaction['save_button'].configure(command=lambda: save_input_configs(
        [gui_components, settings]
    ))

    def async_launch():
        threading.Thread(target=asyncio.run, args=(launch(gui_components, settings),)).start()

    interaction['launch_button'].configure(command=async_launch)

    interaction['res_button'].configure(command=lambda: quit_vr_mode(
        "vorpControl.exe",
        os.path.join(gui_components['sc_entry'].get(), "Bin64/dxgi.dll"),
        os.path.join(gui_components['sc_entry'].get(), "user/client/0/Profiles/default/attributes.xml"),
        gui_components['additional_popup'].get(),
        99999
    ))
    
    if config:
        for key, value in config.items():
            # if key exists in gui_components, set its value
            entry_name = key.replace("_val", "")
            if entry_name in gui_components:
                try:
                    gui_components[entry_name].insert(0, config.get(key, ''))
                except AttributeError:
                    # if the component is not an Entry, set its value directly
                    gui_components[entry_name].set(config.get(key))
            elif (entry_name in settings):
                try:
                    settings[entry_name].insert(0, config.get(key, ''))
                except AttributeError:
                    # if the component is not an Entry, set its value directly
                    settings[entry_name].set(config.get(key))


    else:
        if os.path.exists(STARCITIZEN_DEFAULT):
            gui_components['sc_entry'].insert(0, STARCITIZEN_DEFAULT)
        if os.path.exists(VORPX_DEFAULT):
            gui_components['vorpx_entry'].insert(0, VORPX_DEFAULT)
        if os.path.exists(LAUNCHER_DEFAULT):
            gui_components['launcher_entry'].insert(0, LAUNCHER_DEFAULT)


    root.mainloop()
