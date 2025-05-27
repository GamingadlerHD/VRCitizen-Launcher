# utilities.py
import asyncio
import os
import shutil
import ctypes
import subprocess
import time
import psutil
from constants import HOSTS_FILE, BYPASS_LINE

def is_admin():
    try:
        return os.getuid() == 0
    except AttributeError:
        return ctypes.windll.shell32.IsUserAnAdmin()

def backup_file(src, backup_suffix=".backup"):
    backup_path = src + backup_suffix
    shutil.copy2(src, backup_path)
    return backup_path

def replace_file(src, dst):
    shutil.copy2(src, dst)

def modify_hosts(add=True):
    with open(HOSTS_FILE, "r+", encoding='utf-8') as f:
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

async def wait_for_process(name_substring):
    print(f"Waiting for process containing: {name_substring}")
    while True:
        for proc in psutil.process_iter(['pid','name']):
            if name_substring.lower() in proc.info['name'].lower():
                print(f"Found process: {proc.info['name']}")
                await asyncio.sleep(1)
                return proc
        time.sleep(1)

async def wait_for_exit(proc :str):
    for p in psutil.process_iter(['pid', 'name']):
        if proc.lower() in p.info['name'].lower():
            p.wait()
            return
    raise ValueError(f"No process found with name containing: {proc}")

def is_process_running(name_substring):
    any(name_substring.lower() in proc.info['name'].lower() for proc in psutil.process_iter(['pid', 'name']))

def kill_process_by_name(name_substring):
    for proc in psutil.process_iter(['pid', 'name']):
        if name_substring.lower() in proc.info['name'].lower():
            proc.kill()