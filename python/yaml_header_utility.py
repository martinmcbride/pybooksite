# Author:  Martin McBride
# Created: 2022-05-12
# Copyright (c) 2022, Martin McBride
# License: MIT

# Utility to manipulate yaml headers

import webpages
import yaml
import os


def process_file(filepath, name, process):
    """
    Process a file
    :param filepath: Full path of file to process
    :param process: function that accepts a yaml dictionary and returns a new yaml dictionary
    :return:
    """
    yaml_str, content = webpages.read_webpage_file(filepath, "", name)
    yaml_dict = webpages.parse_yaml(yaml_str, None, None)
    yaml_dict = process(yaml_dict)

    with open(os.path.join(filepath, name), "w") as outfile:
        outfile.write("---\n")
        yaml.dump(yaml_dict, outfile)
        outfile.write("---\n")
        outfile.write(content)

def apply_all(folder, process):
    for dirpath, dirs, files in os.walk(folder):
        print(dirpath, files)
        for filename in files:
            if filename.endswith(".md"):
                process_file(dirpath, filename, process)

def process_add_tag(tag, value):
    def inner(yaml_dict):
        yaml_dict[tag] = value
        return yaml_dict

    return inner

#process_file("/nas/martin/github/pybooksite/sample-site/content/pybooksite/chapter2/", "page1.md", lambda x: x)
apply_all("/nas/martin/github/pybooksite/sample-site/content/", process_add_tag("test_tag", "test_value"))
