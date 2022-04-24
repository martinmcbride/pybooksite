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

    :return: Config object (a dictionary of items)
    """
    try:
        with open("config.yaml") as infile:
            yaml_data = "".join(infile)
        config = yaml.load(yaml_data, yaml.SafeLoader)
    except Exception as e:
        print("Error reading config.yaml")
        print(e)
        raise

    required_keys = ["theme", "site-name", "site-url"]
    error_found = False

    for key in required_keys:
        if key not in config:
            print("config.yaml must specify a", key)
            error_found = True

    if error_found:
        raise Exception()

    if "menu" in config:
        config["menu"] = [{"title": k, "link": v} for k,v in config["menu"].items()]

    if "social" in config:
        config["social"] = [{"title": k, "link": v} for k,v in config["social"].items()]

    return config