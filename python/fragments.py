# Author:  Martin McBride
# Created: 2022-05-13
# Copyright (c) 2022, Martin McBride
# License: MIT
import logging
import os

def get_fragments(config):

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

    for key in list(dynamic_config.keys()):
        if key.startswith("__"):
            fragment_name = dynamic_config[key]
            if not fragment_name in fragments_dict:
                logging.warning("Fragment {} not found in page {}".format(fragment_name, dynamic_config.get("title", "unknown")))
            dynamic_config[key] = fragments_dict.get(fragment_name, None)