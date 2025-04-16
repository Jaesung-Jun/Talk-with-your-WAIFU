import yaml

DEFAULT_FILE_PATH = "settings.yaml"

def parse_settings(file_path=DEFAULT_FILE_PATH):
    with open(file_path, 'r', encoding='utf-8') as file:
        settings = yaml.safe_load(file)

    for key in settings:
        temp = dict()
        for setting_dict in settings[key]:
            temp = {**temp, **setting_dict}
        settings[key] = temp
    return settings