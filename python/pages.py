# Author:  Martin McBride
# Created: 2022-04-16
# Copyright (c) 2022, Martin McBride
# License: MIT

import os
import yaml
import markdown

def read_page_file(base, path, name):
    """
    Read a page file consisting of a yaml header and a markdown body (both optional)

    File format uses a line "---" as a separator. Th etwo sperators must be present even if the yaml data is empty:

    ---
    yaml data
    ---
    markdown data

    :param base: base path to content area
    :param path: path of this page within the content area
    :param name: name of md file
    :return: (yaml, markdown) data as strings. Either string may be empty if the corresponding data isn't present.
    """

    try:
        with open(os.path.join(base, path, name)) as infile:
            yaml_data = ''
            markdown_data = ''
            for s in infile:
                if s.startswith('---'):
                    break;
            for s in infile:
                if s.startswith('---'):
                    break;
                else:
                    yaml_data += s
            for s in infile:
                markdown_data += s
    except Exception as e:
        print("Error reading markdown file", path, name)
        print(e)
        raise

    return yaml_data, markdown_data


def parse_yaml(yaml_data, path, name):
    """
    Load the yaml data

    For flexibility, this will return a dictionary of all keys in the yaml data. Single entries are returned as strings,
    multiple entries are returned as lists.

    New themes can potentially add new keys.

    :param yaml_data: yaml data extracted from markdown file
    :param path: path of this page within the content area
    :param name: name of md file
    :return: yaml dictionary object (a dictionary of items)
    """
    try:
        yaml_dict = yaml.load(yaml_data, yaml.SafeLoader)
    except Exception as e:
        print("Error parsing yaml data in markdown file", path, name)
        print(e)
        raise

    return yaml_dict

def convert_markdown_to_html(markdown_data, path, name):
    """
    Convert a markdown string to
    :param markdown_data: the markdown data from source file
    :param path: path of this page within the content area
    :param name: name of md file
    :return: html data as a string
    """
    try:
        html = markdown.markdown(markdown_data, extensions=['codehilite', 'fenced_code', 'tables', 'customblocks'])
    except Exception as e:
        print("Error parsing markdown data in markdown file", path, name)
        print(e)
        raise
    return html


def create_page_dictionary(yaml_dict, html, path, name):
    """
    Create a page dictionary. This is basically the yaml_dict with:

      - html content added as content item
      - output path added as path item
      - various other tags set to default values to make subsequent processing easier

    :param yaml_dict: yaml data for page - this will be modified
    :param html: page markdown converted to html (the page content)
    :param path: path of this page within the content area
    :param name: name of md file
    :return: page dictionary - final destination of the file in the
    """

    # Add the content
    yaml_dict["content"] = html

    # Create a path.
    # Each html file is renamed to index.html and stored in its own directory, so the full path is formed by joining the
    # path and the name. The exception is for files that are named index - they are stored in the origianl folder.
    name = os.path.splitext(name)[0]
    if name!='index':
        path = "/".join((path, name))
    yaml_dict["path"] = path


    # If short title is not present, use the title instead
    yaml_dict["shorttitle"] = yaml_dict.get("shorttitle", yaml_dict.get("title", ""))

    # tags and categories should be empty tuple if not present
    yaml_dict["tags"] = yaml_dict.get("tags", [])
    yaml_dict["categories"] = yaml_dict.get("categories", [])

    return yaml_dict

def load_page(config, base, path, name):
    """
    Load a page md file
    :param config: main site configuration config.yaml
    :param base: base path to content area
    :param path: path of this page within the content area
    :param name: name of md file
    :return: A page dictionary, or None if the page should be ignored (eg if draft is true)
    """
    yaml_data, markdown_data = read_page_file(base, path, name)

    yaml_dict = parse_yaml(yaml_data, path, name)

    if yaml_dict.get("draft", False):  # If page is draft, return None to indicate it should be ignored.
        return None

    html = convert_markdown_to_html(markdown_data, path, name)

    title = yaml_dict.get('title', '')
    series = '' if not yaml_dict.get('series') else yaml_dict.get('series')[0]

    page_dict = create_page_dictionary(yaml_dict, html, path, name)
    return page_dict

def load_pages(config):
    """
    Load all md files under the content folder.
    :param config: main site configuration config.yaml
    :return: A list of pages
    """
    base = "content"
    pages = []
    for subdir, dirs, files in os.walk(base):
        for filename in files:
            path = subdir[len(base)+1:]
            print(">>>", base, path, filename)
            if filename.endswith(".md"):
                page = load_page(config, base, path, filename)
                if page:
                    pages.append(page)
    return pages
