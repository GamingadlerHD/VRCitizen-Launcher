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
    config.read(ini_path, encoding='utf-8')

    if not config.has_section(section):
        config.add_section(section)
    
    if not config.has_option(section, key):
        config.set(section, key, str(value))
    else:
        current_value = config.get(section, key)
        if current_value != str(value):
            config.set(section, key, str(value))

    with open(ini_path, 'w', encoding='utf-8') as configfile:
        config.write(configfile)

def add_item_to_list_if_needed(exe_name, file_path):
    config = configparser.ConfigParser()
    config.read(file_path)

    if 'Excludes' not in config:
        config['Excludes'] = {}

    excludes = config['Excludes']

    # Prüfen, ob exe schon vorhanden ist
    if exe_name.lower() in (v.lower() for v in excludes.values()):
        print(f"{exe_name} ist bereits enthalten.")
        return

    # Nächsten verfügbaren Schlüssel finden
    index = 100
    while f'excl{index}' in excludes:
        index += 1

    # Hinzufügen
    excludes[f'excl{index}'] = exe_name

    # Datei speichern
    with open(file_path, 'w') as configfile:
        config.write(configfile)
    print(f"{exe_name} wurde hinzugefügt als excl{index}.")