# Author:  Martin McBride
# Created: 2022-05-13
# Copyright (c) 2022, Martin McBride
# License: MIT
import logging
import os

def get_fragments(config):
    """
    Go to fragments directory of current theme. For each file, read the content and store it in the
    fragments dictionary using the filename as a key.
    :param config: Config dictionary
    :return: Dictionary of fragment contents
    """

    fragments_dict = dict()
    theme = config["theme"]
    fragments_path = os.path.join("themes", theme, "fragments")

    for dirpath, dirs, files in os.walk(fragments_path):
        for file in files:
            file_path = os.path.join(dirpath, file)
            with open(file_path) as infile:
                fragments_dict[file] = "\n".join(infile)

    return fragments_dict

def replace_fragments(fragments_dict, dynamic_config):
    """
    Replaces fragment place holders in dynamic config with config content.

    For example:

    * fragments_dict contains two entries:
        * ad1.html: <content of ad1.html file>
        * ad2.html: <content of ad2.html file>

    * dynamic_config contains __advert: ad1.html (which comes from page yaml)

    * This code will update dynamic config with __advert: <content of ad1.html file>

    * Theme template wil include {{__advert}} that will then be replaced with <content of ad1.html file> when
      pystache runs.

    :param fragments_dict: Dictionary containing fragments
    :param dynamic_config: Dynamic page config dictionary
    :return:
    """

    for key in list(dynamic_config.keys()):
        if key.startswith("__"):
            fragment_name = dynamic_config[key]
            if not fragment_name in fragments_dict:
                logging.warning("Fragment {} not found in page {}".format(fragment_name, dynamic_config.get("title", "unknown")))
            dynamic_config[key] = fragments_dict.get(fragment_name, None)
