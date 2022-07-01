# Author:  Martin McBride
# Created: 2022-04-16
# Copyright (c) 2022, Martin McBride
# License: MIT

import yaml
import logging

def read_config_file(filepath):
    """
    Read the config file.
    Raises an exception if this fails.
    :param filepath: Path of config file
    :return: config data (yaml dictionary)
    """
    try:
        with open("config.yaml") as infile:
            yaml_data = "".join(infile)
        return yaml.load(yaml_data, yaml.SafeLoader)
    except Exception as e:
        logging.error("Error reading config.yaml")
        logging.error(str(e))
        raise

def check_required_keys(config):
    """
    Check if necessary keys are contained in the config data.
    Raises an exception if not.
    :param config: config data (yaml dictionary)
    :return: None
    """
    required_keys = ["theme", "site-name", "site-url", "public"]
    error_found = False

    for key in required_keys:
        if key not in config:
            logging.error("config.yaml must contain a {} entry".format(key))
            error_found = True

    if error_found:
        raise Exception()

def expand_menu_items_if_present(key, config):
    """
    A menu item (for example the main menu) in the config file consists of a list of (title, link) pairs.

    For pystache, a menu needs to be stored as a list of dictionaries, where each dictionary contains

    {"title": title, "link": link}

    This function checks is the key exists in the config, and if it does it transforms the data as described. The
    transformed data is written back with the same tag name.

    :param key:
    :param config:
    :return:
    """
    if key in config:
        config[key] = [{"title": k, "link": v} for k,v in config[key].items()]


def load_config():
    """
    Load the configuration yaml file from default location ./config.yaml

    For flexibility, this will return a dictionary of all keys in the yaml file. Single entries are returned as strings,
    multiple entries are returned as lists.

    New themes can potentially add new keys.

    :return: Config object (a dictionary of items)
    """
    config = read_config_file("config.yaml")

    check_required_keys(config)

    # Expand main menu and social menu items for use with pystache
    expand_menu_items_if_present("menu", config)
    expand_menu_items_if_present("social", config)

    return config
