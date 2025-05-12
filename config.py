# config.py
import json
import os
from constants import CONFIG_FILE

def load_input_config():
    if not os.path.exists(CONFIG_FILE):
        return None
    with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
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
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f)

def add_or_change_value_in_config(key: str, value: str):
    config = load_input_config()
    if config is None:
        config = {}
    config[key] = value
    with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
        json.dump(config, f)
