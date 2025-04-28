# utilities.py
import os
import shutil
import subprocess
import time
import psutil
from constants import HOSTS_FILE, BYPASS_LINE

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