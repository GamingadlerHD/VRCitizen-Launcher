import configparser


def get_ini_content(ini_path):
    config = configparser.ConfigParser()

    config.read(ini_path, encoding='utf-8')
    ini_content = {}

    for section in config.sections():
        ini_content[section] = {}
        for key, value in config.items(section):
            ini_content[section][key] = value
    
    return ini_content

def update_or_add_ini_property(ini_path, section, key, value):
    config = configparser.ConfigParser()
    config.optionxform = str
    config.read(ini_path, encoding='utf-8')

    if not config.has_section(section):
        config.add_section(section)
    
    if not config.has_option(section, key):
        config.set(section, key, str(value))
    else:
        current_value = config.get(section, key)
        if current_value != str(value):
            config.set(section, key, str(value))
        else:
            return False

    with open(ini_path, 'w', encoding='utf-8') as configfile:
        config.write(configfile)
    return True

def add_item_to_list_if_needed(value, file_path, section='Exclude', prefix='sExcl'):
    config = configparser.ConfigParser()
    config.read(file_path)

    if section not in config:
        config[section] = {}

    excludes = config[section]

    if value.lower() in (v.lower() for v in excludes.values()):
        print(f"{value} already present.")
        return False

    index = 0
    while f'{prefix}{index}' in excludes:
        index += 1

    update_or_add_ini_property(file_path, section, f'{prefix}{index}', value)
    return True