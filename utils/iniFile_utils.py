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

def update_ini_property(ini_path, section, key, value):
    config = configparser.ConfigParser()
    config.read(ini_path, encoding='utf-8')

    if not config.has_section(section):
        config.add_section(section)
    
    config.set(section, key, str(value))

    with open(ini_path, 'w', encoding='utf-8') as configfile:
        config.write(configfile)
