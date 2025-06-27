# utilities.py
import asyncio
import os
import shutil
import ctypes
import psutil
from constants import HOSTS_FILE, BYPASS_LINE
from logs import log, warn, error

def is_admin():
    try:
        result = os.getuid() == 0
        log(f"Administrator check (Unix): {result}")
        return result
    except AttributeError:
        result = ctypes.windll.shell32.IsUserAnAdmin()
        log(f"Administrator check (Windows): {result}")
        return result

def backup_file(src, backup_suffix=".backup"):
    log(f"Creating backup of file: {src}")
    backup_path = src + backup_suffix
    if not os.path.exists(backup_path):
        try:
            shutil.copy2(src, backup_path)
            log(f"Backup created successfully: {backup_path}")
        except Exception as e:
            error(f"Failed to create backup of {src}: {e}")
            raise
    else:
        log(f"Backup already exists: {backup_path}")
    return backup_path

def replace_file(src, dst):
    log(f"Replacing file: {dst} with {src}")
    try:
        shutil.copy2(src, dst)
        log("File replaced successfully")
    except Exception as e:
        error(f"Failed to replace file {dst} with {src}: {e}")
        raise

def modify_hosts(add=True):
    action = "Adding to" if add else "Removing from"
    log(f"{action} hosts file: {HOSTS_FILE}")
    try:
        with open(HOSTS_FILE, "r+", encoding='utf-8') as f:
            lines = f.readlines()
            f.seek(0)
            if add:
                if BYPASS_LINE not in lines:
                    lines.append(BYPASS_LINE)
                    log("Added bypass line to hosts file")
                else:
                    log("Bypass line already exists in hosts file")
            else:
                original_count = len(lines)
                lines = [line for line in lines if line != BYPASS_LINE]
                if len(lines) < original_count:
                    log("Removed bypass line from hosts file")
                else:
                    log("Bypass line not found in hosts file")
            f.truncate(0)
            f.writelines(lines)
    except Exception as e:
        error(f"Failed to modify hosts file: {e}")
        raise

def launch_process(path):
    try:
        ctypes.windll.shell32.ShellExecuteW(None, "open", path, None, None, 1)
    except Exception as e:
        error(f"Failed to launch process {path}: {e}")
        raise

async def wait_for_process(name_substring):
    log(f"Waiting for process containing: {name_substring}")
    while True:
        for proc in psutil.process_iter(['pid','name']):
            if name_substring.lower() in proc.info['name'].lower():
                log(f"Found process: {proc.info['name']}")
                await asyncio.sleep(1)
                return proc
        await asyncio.sleep(1)

async def wait_for_exit(proc :str):
    for p in psutil.process_iter(['pid', 'name']):
        if proc.lower() in p.info['name'].lower():
            p.wait()
            return
    warn(f"No process found with name containing: {proc}")

def is_process_running(name_substring):
    log(f"Checking if process containing: {name_substring} is running")
    return any(name_substring.lower() in proc.info['name'].lower() for proc in psutil.process_iter(['pid', 'name']))

def kill_process_by_name(name_substring):
    killed_count = 0
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            if name_substring.lower() in proc.info['name'].lower():
                proc.kill()
                killed_count += 1
        
        if killed_count == 0:
            log(f"No processes found containing: {name_substring}")
    except Exception as e:
        error(f"Error while killing processes: {e}")
        raise