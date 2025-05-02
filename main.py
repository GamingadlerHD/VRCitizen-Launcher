import tkinter as tk
from tkinter import messagebox
import os
import shutil
from config import save_config, load_config
from xml_editor import update_xml_by_dict
from utilities import *
from GUI.gui import setup_gui
from validation import validate_resolution
from i18n import set_language, translate
from constants import LAUNCHER_DEFAULT, STARCITIZEN_DEFAULT, VORPX_DEFAULT

def launch():
    sc_folder_path = gui_components['sc_entry'].get()
    vorpx_path = gui_components['vorpx_entry'].get()
    launcher_path = gui_components['launcher_entry'].get()
    stay_in_vr = gui_components['stay_in_vr'].get()

    # Derived paths
    eac_folder_path = os.path.join(os.getenv('APPDATA'), "EasyAntiCheat")
    attr_orig_path = os.path.join(sc_folder_path, "user/client/0/Profiles/default/attributes.xml")
    sc_executable = os.path.join(sc_folder_path, "Bin64/StarCitizen.exe")
    dxgi_dest_path = os.path.join(sc_folder_path, "Bin64/dxgi.dll")

    # Pre-Validation
    script_dir = os.getcwd()
    dxgi_path = os.path.join(script_dir, "dxgi.dll")

    if not os.path.isfile(dxgi_path):
        messagebox.showerror(
            translate("error_title"), 
            translate("hook_file_not_found").format(dxgi_path=dxgi_path)
        )
        exit(1)

    if not all([sc_folder_path, vorpx_path]):
        messagebox.showerror(
            translate("error_title"), 
            translate("select_all_files")
        )
        return

    # Path validations
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
    
    if not validate_resolution(int(gui_components['width_entry'].get()), int(gui_components['height_entry'].get())):
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
            messagebox.showinfo(
                translate("info_title"), 
                translate("modifying_hosts")
            )
            backup_file(HOSTS_FILE)
            modify_hosts(add=True)
            doneStepID += 1

            messagebox.showinfo(
                translate("info_title"), 
                translate("pasting_dxgi")
            )
            shutil.copy2(dxgi_path, dxgi_dest_path)
            doneStepID += 1

            messagebox.showinfo(
                translate("info_title"), 
                translate("starting_vorpx")
            )
            launch_process(vorpx_path)
            doneStepID += 1

            messagebox.showinfo(
                translate("info_title"), 
                translate("updating_attributes")
            )
            backup_file(attr_orig_path)
            view_attr = {'width': gui_components['width_entry'].get(), 'height': gui_components['height_entry'].get(), 'FOV': gui_components['fov_entry'].get()}
            update_xml_by_dict(attr_orig_path, view_attr)
            doneStepID += 1

            messagebox.showinfo(
                translate("info_title"), 
                translate("waiting_vorpx_start")
            )
            wait_for_process(vorpx_proc_name)

            messagebox.showinfo(
                translate("info_title"), 
                translate("deleting_eac")
            )
            if not os.path.isdir(eac_folder_path):
                messagebox.showinfo(
                    translate("info_title"), 
                    translate("eac_already_removed")
                )
            else:
                shutil.rmtree(eac_folder_path, ignore_errors=True)
                messagebox.showinfo(
                    translate("info_title"), 
                    translate("eac_removed")
                )
            doneStepID += 1
            
            launch_process(launcher_path)
            messagebox.showinfo(
                translate("info_title"), 
                translate("waiting_launcher_start")
            )

            if (stay_in_vr):
                wait_for_process("StarCitizen")
                messagebox.showinfo(
                    translate("info_title"), 
                    translate("launching_sc")
                )
                wait_for_exit(sc_proc_name)
                quit_vr_mode(vorpx_proc_name, dxgi_dest_path, attr_orig_path, doneStepID)

        except Exception as e:
            messagebox.showerror(
                translate("error_title"), 
                translate("error_occurred_revert").format(e=e)
            )
            quit_vr_mode(vorpx_proc_name, dxgi_dest_path, attr_orig_path, doneStepID)

    except Exception as e:
        messagebox.showerror(
            translate("error_title"), 
            translate("operation_failed").format(e=e)
        )

def quit_vr_mode(vorpx_proc_name, dxgi_dest_path, attr_orig_path, doneStepID):
    try:
        if doneStepID > 0:
            messagebox.showinfo(
                translate("info_title"), 
                translate("restoring_hosts")
            )
            shutil.copy2(HOSTS_FILE + ".backup", HOSTS_FILE)
            os.remove(HOSTS_FILE + ".backup")

        if doneStepID > 1:
            messagebox.showinfo(
                translate("info_title"), 
                translate("removing_dxgi")
            )
            if os.path.exists(dxgi_dest_path):
                os.remove(dxgi_dest_path)

        if doneStepID > 2:
            messagebox.showinfo(
                translate("info_title"), 
                translate("killing_vorpx")
            )
            kill_process_by_name(vorpx_proc_name)

        if doneStepID > 3:
            messagebox.showinfo(
                translate("info_title"), 
                translate("restoring_attributes")
            )
            if os.path.exists(attr_orig_path + ".backup"):
                shutil.copy2(attr_orig_path + ".backup", attr_orig_path)
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
    root = tk.Tk()
    gui_components, settings = setup_gui(root)
    
    # Assign button commands
    gui_components['save_button']['command'] = lambda: save_config(
        gui_components['sc_entry'].get(),
        gui_components['vorpx_entry'].get(),
        gui_components['launcher_entry'].get(),
        gui_components['fov_entry'].get(),
        gui_components['width_entry'].get(),
        gui_components['height_entry'].get(),
        settings
    )
    gui_components['launch_button']['command'] = launch
    gui_components['res_button']['command'] = lambda: quit_vr_mode(
        gui_components['vorpx_entry'].get(),
        os.path.join(gui_components['sc_entry'].get(), "Bin64/dxgi.dll"),
        os.path.join(gui_components['sc_entry'].get(), "user/client/0/Profiles/default/attributes.xml"),
        99999
    )

    # Load config
    config = load_config()
    if config:
        gui_components['sc_entry'].insert(0, config.get('sc_path', ''))
        gui_components['vorpx_entry'].insert(0, config.get('vorpx_path', ''))
        gui_components['fov_entry'].insert(0, config.get('fov', ''))
        gui_components['width_entry'].insert(0, config.get('width', ''))
        gui_components['height_entry'].insert(0, config.get('height', ''))
        gui_components['launcher_entry'].insert(0, config.get('launcher_path', ''))

    else:
        if os.path.exists(STARCITIZEN_DEFAULT):
            gui_components['sc_entry'].insert(0, STARCITIZEN_DEFAULT)
        if os.path.exists(VORPX_DEFAULT):
            gui_components['vorpx_entry'].insert(0, VORPX_DEFAULT)
        if os.path.exists(LAUNCHER_DEFAULT):
            gui_components['launcher_entry'].insert(0, LAUNCHER_DEFAULT)


    root.mainloop()