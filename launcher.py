import tkinter as tk
from tkinter import filedialog, messagebox
import subprocess
import shutil
import time
import os
import sys
import psutil


from pathlib import Path
import json

CONFIG_FILE = 'config.json'


# ==== CONFIG ====
#ATTRIBUTES_FILE_ORIGINAL = r"C:\\Program Files\\Roberts Space Industries\\StarCitizen\\LIVE\\user\\client\\0\\Profiles\\default\\attributes.xml"
HOSTS_FILE = r"C:\\Windows\\System32\\drivers\\etc\\hosts"

# Placeholder bypass line
BYPASS_LINE = "127.0.0.1 modules-cdn.eac-prod.on.epicgames.com\n"

def save_config(sc_path, vorpx_path, eac_folder):
    config = {
        "sc_path": sc_path,
        "vorpx_path": vorpx_path,
        "eac_folder": eac_folder
    }
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return None
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)



# === FUNCTIONS ===

def is_admin():
    try:
        return os.getuid() == 0
    except AttributeError:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()

def backup_file(src, backup_suffix=".backup"):
    backup_path = src + backup_suffix
    shutil.copy2(src, backup_path)
    return backup_path

def replace_file(src, dst):
    shutil.copy2(src, dst)

def modify_hosts(add=True):
    with open(HOSTS_FILE, "r+") as f:
        lines = f.readlines()
        f.seek(0)
        if add:
            if BYPASS_LINE not in lines:
                lines.append(BYPASS_LINE)
        else:
            lines = [line for line in lines if line != BYPASS_LINE]
        f.truncate(0)
        f.writelines(lines)

def launch_process(path):
    return subprocess.Popen(path, shell=True)

def wait_for_process(name_substring):
    while True:
        for proc in psutil.process_iter(['name']):
            if proc.info['name'] and name_substring.lower() in proc.info['name'].lower():
                return proc
        time.sleep(1)

def wait_for_exit(proc):
    proc.wait()

def kill_process_by_name(name_substring):
    for proc in psutil.process_iter(['pid', 'name']):
        if name_substring.lower() in proc.info['name'].lower():
            proc.kill()

# === GUI ===

def browse_file(entry, filetypes):
    filename = filedialog.askopenfilename(filetypes=filetypes)
    if filename:
        entry.delete(0, tk.END)
        entry.insert(0, filename)

def browse_folder(entry):
    foldername = filedialog.askdirectory()
    if foldername:
        entry.delete(0, tk.END)
        entry.insert(0, foldername)


def launch():
    sc_folder_path = sc_entry.get()
    vorpx_path = vorpx_entry.get()
    attr_orig_path = os.path.join(sc_folder_path, "/user/client/0/Profiles/default/attributes.xml")
    sc_executable = os.path.join(sc_folder_path, "/Bin64/StarCitizen.exe")
    dxgi_dest_path = os.path.join(os.path.dirname(sc_folder_path, "/Bin64/dxgi.dll"))
    eac_folder_path = eac_folder_entry.get()
    
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

    # check if all paths are valid
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
        # Initialize variables to track changes
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
            # Revert changes in reverse order
            messagebox.showerror("Error", f"An error occurred: {e}\nAttempting to revert changes...")
        
            try:
                # Restore attributes if they were modified
                if attr_modified and os.path.exists(attr_orig_path + ".backup"):
                    shutil.copy2(attr_orig_path + ".backup", attr_orig_path)
                    os.remove(attr_orig_path + ".backup")
                    messagebox.showinfo("Info", "Restored original attributes file")
                
                # Restore hosts file if it was modified
                if hosts_modified and os.path.exists(HOSTS_FILE + ".backup"):
                    shutil.copy2(HOSTS_FILE + ".backup", HOSTS_FILE)
                    os.remove(HOSTS_FILE + ".backup")
                    messagebox.showinfo("Info", "Restored original hosts file")

                if inserted_dxgi and os.path.exists(dxgi_dest_path):
                    os.remove(dxgi_dest_path)
                    messagebox.showinfo("Info", "Removed dxgi.dll hook file")
                
                # Kill vorpX if it was launched
                if vorpx_proc is not None:
                    try:
                        kill_process_by_name(vorpx_proc_name)
                        messagebox.showinfo("Info", "Closed vorpX process")
                    except:
                        pass
                
                    
            except Exception as revert_error:
                messagebox.showerror("Revert Error", f"Failed to fully revert changes: {revert_error}")

    except Exception as e:
        messagebox.showerror("Error", f"Operation failed: {e}")

# --- Build GUI
root = tk.Tk()
root.title("Star Citizen VR Launcher")


# Star Citizen Exe
tk.Label(root, text="Star Citizen Exe").grid(row=0, column=0)
sc_entry = tk.Entry(root, width=50)
sc_entry.grid(row=0, column=1)
tk.Button(root, text="Browse", command=lambda: browse_folder(sc_entry)).grid(row=0, column=2)

# VorpX Exe
tk.Label(root, text="vorpX Exe").grid(row=1, column=0)
vorpx_entry = tk.Entry(root, width=50)
vorpx_entry.grid(row=1, column=1)
tk.Button(root, text="Browse", command=lambda: browse_file(vorpx_entry, [('Executables', '*.exe')])).grid(row=1, column=2)

# EasyAntiCheat Folder
tk.Label(root, text="EasyAntiCheat Folder").grid(row=2, column=0)
eac_folder_entry = tk.Entry(root, width=50)
eac_folder_entry.grid(row=3, column=1)
tk.Button(root, text="Browse", command=lambda: browse_folder(eac_folder_entry)).grid(row=2, column=2)

# Original Attributes File
tk.Label(root, text="Original Attributes File").grid(row=3, column=0)
attr_orig_entry = tk.Entry(root, width=50)
attr_orig_entry.grid(row=3, column=1)
tk.Button(root, text="Browse", command=lambda: browse_file(attr_orig_entry, [('XML Files', '*.xml')])).grid(row=3, column=2)

# Buttons
tk.Button(root, text="Save Config", command=lambda: save_config(
    sc_entry.get(), vorpx_entry.get(), attr_orig_entry.get(), eac_folder_entry.get())
).grid(row=5, column=0)
tk.Button(root, text="Launch", command=launch).grid(row=5, column=1)



config = load_config()
if config:
    sc_entry.insert(0, config.get('sc_path', ''))
    vorpx_entry.insert(0, config.get('vorpx_path', ''))
    eac_folder_entry.insert(0, config.get('eac_folder', ''))

root.mainloop()