# config.py
import json
import os
from constants import CONFIG_FILE

def save_config(sc_path, vorpx_path, launcher_path, fov, width, height, settings):
    config = {
        "sc_path": sc_path,
        "vorpx_path": vorpx_path,
        "launcher_path": launcher_path,
        "fov": fov,
        "width": width,
        "height": height,
        "game_settings": settings
    }
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)

def load_config():
    if not os.path.exists(CONFIG_FILE):
        return None
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)