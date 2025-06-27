# config.py
import json
import os
from constants import CONFIG_FILE
from logs import log, warn, error

def load_input_config():
    if not os.path.exists(CONFIG_FILE):
        log("Configuration file does not exist")
        return None
    try:
        with open(CONFIG_FILE, 'r', encoding='utf-8') as f:
            config = json.load(f)
            log(f"Configuration loaded successfully with {len(config)} entries")
            return config
    except Exception as e:
        error(f"Failed to load configuration: {e}")
        return None
    
def save_input_configs(ui_components: list[dict]):
    log("Saving input configurations...")
    config : dict = {}
    component_count = 0
    
    try:
        for component in ui_components:
            for key, value in component.items():
                config_name = key + "_val"
                try:
                    config[config_name] = value.get()
                    component_count += 1
                except AttributeError:
                    config[config_name] = value
                    component_count += 1
        
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f, indent=2)
        
        log(f"Successfully saved {component_count} configuration values to {CONFIG_FILE}")
    except Exception as e:
        error(f"Failed to save configuration: {e}")
        raise

def add_or_change_value_in_config(key: str, value: str):
    try:
        config = load_input_config()
        if config is None:
            config = {}
        config[key] = value
        with open(CONFIG_FILE, 'w', encoding='utf-8') as f:
            json.dump(config, f)
    except Exception as e:
        error(f"Failed to update configuration: {e}")
