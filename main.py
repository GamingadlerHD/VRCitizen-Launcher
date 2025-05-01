# main.py
import tkinter as tk
from tkinter import messagebox
import os
import shutil
from config import save_config, load_config
from xml_editor import update_attributes
from utilities import *
from gui import setup_gui
from validation import validate_resolution
from i18n import set_language, translate

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
        messagebox.showerror("Error", f"Required vorpX hook file not found:\n{dxgi_path}")
        exit(1)

    if not all([sc_folder_path, vorpx_path]):
        messagebox.showerror("Error", "Please select all necessary files!")
        return

    # Path validations
    if not os.path.isdir(sc_folder_path):
        messagebox.showerror("Error", f"Star Citizen folder not found:\n{sc_folder_path}")
        return
    if not os.path.isfile(vorpx_path):
        messagebox.showerror("Error", f"vorpX executable not found:\n{vorpx_path}")
        return 
    if not os.path.isfile(sc_executable):
        messagebox.showerror("Error", f"Star Citizen executable not found:\n{sc_executable}")
        return
    if not os.path.isfile(attr_orig_path):
        messagebox.showerror("Error", f"Original attributes file not found:\n{attr_orig_path}")
        return

    if not is_admin():
        messagebox.showerror("Admin Required", "This launcher must be run as administrator!")
        return
    
    if not validate_resolution(int(gui_components['width_entry'].get()), int(gui_components['height_entry'].get())):
        messagebox.showerror("Error", "Your monitor resolution is to small for the selected VR resolution. Visit xyz for more information.")
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


            messagebox.showinfo("Info", "Modifying hosts file...")
            backup_file(HOSTS_FILE)
            modify_hosts(add=True)
            doneStepID += 1

            messagebox.showinfo("Info", "Pasting dxgi.dll... (Hook Helper)")
            shutil.copy2(dxgi_path, dxgi_dest_path)
            doneStepID += 1

            messagebox.showinfo("Info", "Starting vorpX...")
            launch_process(vorpx_path)
            doneStepID += 1

            messagebox.showinfo("Info", "Updating attributes file...")
            backup_file(attr_orig_path)
            update_attributes(attr_orig_path, width=gui_components['width_entry'].get(), height=gui_components['height_entry'].get(), fov=gui_components['fov_entry'].get())
            doneStepID += 1

            messagebox.showinfo("Info", "Waiting for vorpX to fully start...")
            wait_for_process(vorpx_proc_name)

            messagebox.showinfo("Info", "Deleting EasyAntiCheat folder...")
            if not os.path.isdir(eac_folder_path):
                messagebox.showinfo("Info", "EasyAntiCheat folder already removed.")
            else:
                shutil.rmtree(eac_folder_path, ignore_errors=True)
                messagebox.showinfo("Info", "EasyAntiCheat folder removed.")
            doneStepID += 1

            
            launch_process(launcher_path)
            messagebox.showinfo("Info", "Waiting for RSI Launcher to fully start...")

            
            if (stay_in_vr):
                wait_for_process("StarCitizen")
                messagebox.showinfo("Info", "Launching Star Citizen...")
                wait_for_exit(sc_proc_name)
                quit_vr_mode(vorpx_proc_name, dxgi_dest_path, attr_orig_path, doneStepID)


        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}\nAttempting to revert changes...")
            # Revert logic here...
            quit_vr_mode(vorpx_proc_name, dxgi_dest_path, attr_orig_path, doneStepID)

    except Exception as e:
        messagebox.showerror("Error", f"Operation failed: {e}")



def quit_vr_mode(vorpx_proc_name, dxgi_dest_path, attr_orig_path, doneStepID):
    # Logic to quit VR mode
    try:
        if doneStepID > 0:
            messagebox.showinfo("Info", "Restoring hosts file...")
            shutil.copy2(HOSTS_FILE + ".backup", HOSTS_FILE)
            os.remove(HOSTS_FILE + ".backup")

        if doneStepID > 1:
            messagebox.showinfo("Info", "Removing dxgi.dll...")
            if os.path.exists(dxgi_dest_path):
                os.remove(dxgi_dest_path)

        if doneStepID > 2:
            messagebox.showinfo("Info", "Killing vorpX process...")
            kill_process_by_name(vorpx_proc_name)

        if doneStepID > 3:
            messagebox.showinfo("Info", "Restoring original attributes...")
            if os.path.exists(attr_orig_path + ".backup"):
                shutil.copy2(attr_orig_path + ".backup", attr_orig_path)
                os.remove(attr_orig_path + ".backup")


        messagebox.showinfo("Successfully Restored", "Everything has been restored to its original state.")

    except Exception as e:
        messagebox.showerror("Error", f"An error occurred while quitting VR mode: {e}")

    return



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
        settings['lang'].get()
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
        
        set_language(config.get('lang', ''))

    root.mainloop()