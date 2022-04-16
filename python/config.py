# Author:  Martin McBride
# Created: 2022-04-16
# Copyright (c) 2022, Martin McBride
# License: MIT

import yaml

def load_config():
    """
    Load the configuration yaml file from default location ./config.yaml

    For flexibility, this will return a dictionary of all keys in the yaml file. Single entries are returned as strings,
    multiple entries are returned as lists.

    New themes can potentially add new keys.

    :return: Config object (a dictionary of items
    """
    try:
        with open("./config.yaml") as infile:
            yaml_data = ''.join(infile)
        config = yaml.load(yaml_data, yaml.SafeLoader)
    except Exception as e:
        print("Error reading config.yaml")
        print(e)
        raise

    if not config.get("theme", ""):
        print("config.yaml must specify a theme")
        raise Exception()

    return config