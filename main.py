import tkinter as tk
from tkinter import messagebox
import os
import sys  # pylint: disable=unused-import
import ctypes  # pylint: disable=unused-import
import shutil
from config import save_input_configs, load_input_config
from xml_editor import update_vr_settings_from_xml_to_xml, update_xml_by_dict
from utilities import is_admin, modify_hosts, backup_file, launch_process, wait_for_process, wait_for_exit, kill_process_by_name
from GUI.gui import setup_gui
from validation import validate_resolution
from i18n import set_language, translate
from constants import LAUNCHER_DEFAULT, STARCITIZEN_DEFAULT, VORPX_DEFAULT, HOSTS_FILE

def launch(ui_elements, launcher_settings):
    '''
    Applys all the settings and launches the sc launcher
    '''
    for component_name, component_value in ui_elements.items():
        print(f"{component_name} {component_value.get()}")
    sc_folder_path = ui_elements['sc_entry'].get()
    vorpx_path = ui_elements['vorpx_entry'].get()
    launcher_path = ui_elements['launcher_entry'].get()
    stay_in_vr = ui_elements['stay_in_vr'].get()
    addidional_popups = ui_elements['addidional_popup'].get()

    # Derived paths
    eac_folder_path = os.path.join(os.getenv('APPDATA'), "EasyAntiCheat")
    attr_orig_path = os.path.join(sc_folder_path, "user/client/0/Profiles/default/attributes.xml")
    sc_executable = os.path.join(sc_folder_path, "Bin64/StarCitizen.exe")
    dxgi_dest_path = os.path.join(sc_folder_path, "Bin64/dxgi.dll")

    # Pre-Validation
    script_dir = os.getcwd()
    dxgi_path = os.path.join(script_dir, "dxgi.dll")

    if not all([sc_folder_path, vorpx_path]):
        messagebox.showerror(
            translate("error_title"), 
            translate("select_all_files")
        )
        return

    # Path validations
    if bool(ui_elements['use_dxgi']) is True and bool(os.path.isfile(dxgi_path)) is False:
        messagebox.showerror(
            translate("error_title"), 
            translate("hook_file_not_found").format(dxgi_path=dxgi_path)
        )
        return



    if not os.path.isdir(sc_folder_path):
        messagebox.showerror(
            translate("error_title"), 
            translate("sc_folder_not_found").format(sc_folder_path=sc_folder_path)
        )
        return
    if not os.path.isfile(vorpx_path):
        messagebox.showerror(
            translate("error_title"), 
            translate("vorpx_exe_not_found").format(vorpx_path=vorpx_path)
        )
        return 
    if not os.path.isfile(sc_executable):
        messagebox.showerror(
            translate("error_title"), 
            translate("sc_exe_not_found").format(sc_executable=sc_executable)
        )
        return
    if not os.path.isfile(attr_orig_path):
        messagebox.showerror(
            translate("error_title"), 
            translate("attributes_file_not_found").format(attr_orig_path=attr_orig_path)
        )
        return

    if not is_admin():
        messagebox.showerror(
            translate("admin_required_title"), 
            translate("admin_required_message")
        )
        return
    
    if not validate_resolution(int(ui_elements['width_entry'].get()), int(ui_elements['height_entry'].get())):
        if not ui_elements['ign_res_warning'].get():
            messagebox.showerror(
                translate("error_title"), 
                translate("resolution_too_small")
            )
            return
    
    try:
        doneStepID = 0
        # 1 = modify hosts file
        # 2 = paste dxgi.dll
        # 3 = start vorpX
        # 4 = update attributes file
        # 5 = delete EAC folder
        # 6 = start RSI Launcher

        sc_proc_name = os.path.basename(sc_executable)
        vorpx_proc_name = os.path.basename(vorpx_path)
    
        try:
            if (addidional_popups):
                messagebox.showinfo(translate("info_title"), translate("modifying_hosts"))
            backup_file(HOSTS_FILE)
            modify_hosts(add=True)
            doneStepID += 1

            if (ui_elements['use_dxgi']):
                if (addidional_popups):
                    messagebox.showinfo(
                        translate("info_title"), 
                        translate("pasting_dxgi")
                    )
                    shutil.copy2(dxgi_path, dxgi_dest_path)
                    doneStepID += 1

            if (addidional_popups):
                messagebox.showinfo(
                    translate("info_title"), 
                    translate("vorpx_start")
                )
            launch_process(vorpx_path)
            doneStepID += 1

            if (addidional_popups):
                messagebox.showinfo(
                    translate("info_title"), 
                    translate("waiting_vorpx_start")
                )
            backup_file(attr_orig_path)
            view_attr = {'Width': ui_elements['width_entry'].get(), 'Height': ui_elements['height_entry'].get(), 'FOV': ui_elements['fov_entry'].get()}
            doneStepID += 1
            update_xml_by_dict(attr_orig_path, view_attr)

            stVal = {}
            for component_name, component_value in launcher_settings.items():
                stVal[component_name] = component_value.get()
            update_xml_by_dict(attr_orig_path, stVal)

            if (addidional_popups):
                messagebox.showinfo(
                    translate("info_title"), 
                    translate("waiting_vorpx_start")
                )
            wait_for_process(vorpx_proc_name)

            if (addidional_popups):
                messagebox.showinfo(
                    translate("info_title"), 
                    translate("deleting_eac")
                )
        
            if not os.path.isdir(eac_folder_path):
                if (addidional_popups):
                    messagebox.showinfo(
                        translate("info_title"), 
                        translate("eac_already_removed")
                    )
            else:
                shutil.rmtree(eac_folder_path, ignore_errors=True)
                if (addidional_popups):
                    messagebox.showinfo(translate("info_title"), translate("eac_removed"))
            doneStepID += 1
            
            launch_process(launcher_path)
            if (addidional_popups):
                messagebox.showinfo(
                    translate("info_title"), 
                    translate("waiting_launcher_start")
                )

            if (stay_in_vr):
                wait_for_process("StarCitizen")
                if (addidional_popups):
                    messagebox.showinfo(
                        translate("info_title"), 
                        translate("waiting_sc_start")
                    )

                wait_for_exit(sc_proc_name)
                quit_vr_mode(vorpx_proc_name, dxgi_dest_path, attr_orig_path, addidional_popups, doneStepID)

        except Exception as e:
            messagebox.showerror(
                translate("error_title"), 
                translate("error_occurred_revert").format(e=e)
            )
            quit_vr_mode(vorpx_proc_name, dxgi_dest_path, attr_orig_path, addidional_popups, doneStepID)

    except Exception as e:
        messagebox.showerror(
            translate("error_title"), 
            translate("operation_failed").format(e=e)
        )

def quit_vr_mode(vorpx_proc_name, dxgi_dest_path, attr_orig_path, additional_popups, doneStepID):
    try:
        if doneStepID > 0:
            if additional_popups:
                messagebox.showinfo(translate("info_title"), translate("restoring_hosts"))
            if os.path.exists(HOSTS_FILE + ".backup"):
                shutil.copy2(HOSTS_FILE + ".backup", HOSTS_FILE)
                os.remove(HOSTS_FILE + ".backup")

        if doneStepID > 1:
            if additional_popups:
                messagebox.showinfo(translate("info_title"), translate("removing_dxgi"))
            if os.path.exists(dxgi_dest_path):
                os.remove(dxgi_dest_path)

        if doneStepID > 2:
            if additional_popups:
                messagebox.showinfo(translate("info_title"), translate("killing_vorpx"))
            kill_process_by_name(vorpx_proc_name)

        if doneStepID > 3:
            if additional_popups:
                messagebox.showinfo(translate("info_title"), translate("restoring_attributes"))
            if os.path.exists(attr_orig_path + ".backup"):
                update_vr_settings_from_xml_to_xml(
                    attr_orig_path + ".backup", attr_orig_path)
                os.remove(attr_orig_path + ".backup")

        messagebox.showinfo(
            translate("restored_title"), 
            translate("restored_message")
        )

    except Exception as e:
        messagebox.showerror(
            translate("error_title"), 
            translate("error_quitting_vr").format(e=e)
        )

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

    root = tk.Tk()
    root.iconbitmap("i.ico")
    gui_components, settings, interaction = setup_gui(root)
    
    # Assign button commands
    interaction['save_button']['command'] = lambda: save_input_configs(
        [gui_components, settings]
    )
    interaction['launch_button']['command'] = lambda: launch(gui_components, settings)
    interaction['res_button']['command'] = lambda: quit_vr_mode(
        gui_components['vorpx_entry'].get(),
        os.path.join(gui_components['sc_entry'].get(), "Bin64/dxgi.dll"),
        os.path.join(gui_components['sc_entry'].get(), "user/client/0/Profiles/default/attributes.xml"),
        gui_components['addidional_popup'].get(),
        99999
    )
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
