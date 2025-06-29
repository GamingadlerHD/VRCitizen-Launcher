import configparser
from logs import log, error

def get_ini_content(ini_path):
    config = configparser.ConfigParser()

    try:
        config.read(ini_path, encoding='utf-8')
        ini_content = {}

        for section in config.sections():
            ini_content[section] = {}
            for key, value in config.items(section):
                ini_content[section][key] = value
        
        log(f"Successfully read INI file with {len(ini_content)} sections")
        return ini_content
    except Exception as e:
        error(f"ECL1700: Failed to read INI file {ini_path}: {e}")
        return {}

def update_or_add_ini_property(ini_path, section, key, value):
    log(f"Updating INI property: {ini_path} [{section}] {key} = {value}")
    config = configparser.ConfigParser()
    config.optionxform = str
    
    try:
        config.read(ini_path, encoding='utf-8')

        if not config.has_section(section):
            log(f"Creating new INI section: {section}")
            config.add_section(section)
        
        if not config.has_option(section, key):
            log(f"Adding new INI property: {key}")
            config.set(section, key, str(value))
        else:
            current_value = config.get(section, key)
            if current_value != str(value):
                log(f"Updating INI property from '{current_value}' to '{value}'")
                config.set(section, key, str(value))
            else:
                return False

        with open(ini_path, 'w', encoding='utf-8') as configfile:
            for se in config.sections():
                configfile.write(f'[{se}]\n')
                for ky, val in config.items(se):
                    configfile.write(f'{ky}={val}\n')
                configfile.write('\n')
        
        return True
    except Exception as e:
        error(f"ECL1701: Failed to update INI file {ini_path}: {e}")
        return False

def add_item_to_list_if_needed(value, file_path, section='Exclude', prefix='sExcl'):
    log(f"Adding item to INI list if needed: {value} in {file_path} [{section}]")
    config = configparser.ConfigParser()
    
    try:
        config.read(file_path)

        if section not in config:
            log(f"Creating INI section: {section}")
            config[section] = {}

        excludes = config[section]

        if value.lower() in (v.lower() for v in excludes.values()):
            log(f"{value} already present in exclusion list")
            return False

        index = 0
        while f'{prefix}{index}' in excludes:
            index += 1

        update_or_add_ini_property(file_path, section, f'{prefix}{index}', value)
        return True
    except Exception as e:
        error(f"ECL1702: Failed to add item to INI list: {e}")
        return False