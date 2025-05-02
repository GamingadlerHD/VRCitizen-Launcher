# config.py
import json
import os
from constants import CONFIG_FILE

def load_input_config():
    if not os.path.exists(CONFIG_FILE):
        return None
    with open(CONFIG_FILE, 'r') as f:
        return json.load(f)
    
def save_input_configs(ui_components: list[dict]):
    config : dict = {}
    for component in ui_components:
        for key, value in component.items():
            config_name = key + "_val"
            try:
                config[config_name] = value.get()
            except AttributeError:
                config[config_name] = value
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config, f)
