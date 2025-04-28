# main.py
import tkinter as tk
from tkinter import messagebox
import os
import sys
import shutil
from config import save_config, load_config
from utilities import *
from gui import setup_gui

def launch():
    sc_folder_path = gui_components['sc_entry'].get()
    vorpx_path = gui_components['vorpx_entry'].get()
    eac_folder_path = gui_components['eac_folder_entry'].get()
    attr_orig_path = gui_components['attr_orig_entry'].get()

    # Derived paths
    attr_orig_path = os.path.join(sc_folder_path, "user/client/0/Profiles/default/attributes.xml")
    sc_executable = os.path.join(sc_folder_path, "Bin64/StarCitizen.exe")
    dxgi_dest_path = os.path.join(os.path.dirname(sc_folder_path), "Bin64/dxgi.dll")

    # Pre-Validation
    custom_attr_path = os.path.join(os.path.dirname(sys.argv[0]), "attributes.xml")
    dxgi_path = os.path.join(os.path.dirname(sys.argv[0]), "dxgi.dll")

    if not os.path.isfile(custom_attr_path):
        messagebox.showerror("Error", f"Required custom attributes file not found:\n{custom_attr_path}")
        exit(1)
    if not os.path.isfile(dxgi_path):
        messagebox.showerror("Error", f"Required vorpX hook file not found:\n{dxgi_path}")
        exit(1)

    if not all([sc_folder_path, vorpx_path, eac_folder_path]):
        messagebox.showerror("Error", "Please select all necessary files!")
        return

    sc_proc_name = os.path.basename(sc_executable)
    vorpx_proc_name = os.path.basename(vorpx_path)

    # Path validations
    if not os.path.isdir(sc_folder_path):
        messagebox.showerror("Error", f"Star Citizen folder not found:\n{sc_folder_path}")
        return
    if not os.path.isdir(eac_folder_path):
        messagebox.showerror("Error", f"EasyAntiCheat folder not found:\n{eac_folder_path}")
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

    try:
        hosts_modified = False
        attr_modified = False
        inserted_dxgi = False
        vorpx_proc = None
        sc_proc = None
    
        try:
            messagebox.showinfo("Info", "Modifying hosts file...")
            backup_file(HOSTS_FILE)
            modify_hosts(add=True)
            hosts_modified = True

            messagebox.showinfo("Info", "Pasting dxgi.dll... (Hook Helper)")
            shutil.copy2(dxgi_path, dxgi_dest_path)
            inserted_dxgi = True

            messagebox.showinfo("Info", "Starting vorpX...")
            vorpx_proc = launch_process(vorpx_path)

            messagebox.showinfo("Info", "Replacing attributes file...")
            backup_file(attr_orig_path)
            replace_file(custom_attr_path, attr_orig_path)
            attr_modified = True

            messagebox.showinfo("Info", "Waiting for vorpX to fully start...")
            wait_for_process(vorpx_proc_name)

            messagebox.showinfo("Info", "Launching Star Citizen...")
            sc_proc = launch_process(sc_executable)
            wait_for_exit(sc_proc)

            messagebox.showinfo("Info", "Closing vorpX...")
            kill_process_by_name(vorpx_proc_name)

            messagebox.showinfo("Info", "Removing dxgi.dll...")
            if os.path.exists(dxgi_dest_path):
                os.remove(dxgi_dest_path)
                inserted_dxgi = False

            messagebox.showinfo("Info", "Restoring original attributes...")
            shutil.copy2(attr_orig_path + ".backup", attr_orig_path)
            os.remove(attr_orig_path + ".backup")
            attr_modified = False

            messagebox.showinfo("Info", "Restoring hosts file...")
            shutil.copy2(HOSTS_FILE + ".backup", HOSTS_FILE)
            os.remove(HOSTS_FILE + ".backup")
            hosts_modified = False

            messagebox.showinfo("Success", "All done! Enjoy!")

        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {e}\nAttempting to revert changes...")
            # Revert logic here...

    except Exception as e:
        messagebox.showerror("Error", f"Operation failed: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    gui_components = setup_gui(root)
    
    # Assign button commands
    gui_components['save_button']['command'] = lambda: save_config(
        gui_components['sc_entry'].get(),
        gui_components['vorpx_entry'].get(),
        gui_components['eac_folder_entry'].get()
    )
    gui_components['launch_button']['command'] = launch

    # Load config
    config = load_config()
    if config:
        gui_components['sc_entry'].insert(0, config.get('sc_path', ''))
        gui_components['vorpx_entry'].insert(0, config.get('vorpx_path', ''))
        gui_components['eac_folder_entry'].insert(0, config.get('eac_folder', ''))

    root.mainloop()