# Author:  Martin McBride
# Created: 2022-04-16
# Copyright (c) 2022, Martin McBride
# License: MIT
import logging
import os
import yaml
import markdown
import fragments
import page_utils

def normalise_webpage_dictionary(page_dict, config):
    # If short title is not present, use the title instead
    page_dict["shorttitle"] = page_dict.get("shorttitle", page_dict.get("title", ""))
    # If seo title is not present, use the sitename + title instead
    page_dict["seotitle"] = page_dict.get("seotitle", " - ".join([config.get("site-name", ""), page_dict.get("title", "")]))

    # tags, categories, and level should be empty tuple if not present
    page_dict["tags"] = page_dict.get("tags", [])
    page_dict["categories"] = page_dict.get("categories", [])

    # Pages are indexable by default. This controls whether page appears in indexes
    page_dict["indexable"] = page_dict.get("indexable", True)



def read_webpage_file(base, path, name):
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
        logging.error("Error reading markdown file", path, name)
        logging.error(e)
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
        logging.error("Error parsing yaml data in markdown file", path, name)
        logging.error(e)
        raise

    return yaml_dict

def convert_markdown_to_html(markdown_data, path, name):
    """
    Convert a markdown string to html
    :param markdown_data: the markdown data from source file
    :param path: path of this page within the content area
    :param name: name of md file
    :return: html data as a string
    """
    try:
        html = markdown.markdown(markdown_data, extensions=['codehilite', 'fenced_code', 'tables', 'customblocks'])
    except Exception as e:
        logging.error("Error parsing markdown data in markdown file", path, name)
        logging.error(e)
        raise
    return html


def create_webpage_dictionary(config, yaml_dict, html, path, name, fragments_dict):
    """
    Create a page dictionary. This is basically the yaml_dict with:

      - html content added as content item
      - output path added as path item
      - various other tags set to default values to make subsequent processing easier

    :param yaml_dict: yaml data for page - this will be modified
    :param html: page markdown converted to html (the page content)
    :param path: file path of this md file within the content area
    :param name: name of md file
    :return: webpage dictionary - final destination of the file in the
    """

    # Add the content
    yaml_dict["content"] = html

    # Create a path.
    yaml_dict["path"] = page_utils.get_webpage_path(path, name)

    normalise_webpage_dictionary(yaml_dict, config)

    # Update fragments with dynamic content
    fragments.replace_fragments(fragments_dict, yaml_dict)

    return yaml_dict


def check_deferred_page(yaml_dict):
    """
    Check data of page against today's date, return true if page date > today's date
    @param yaml_dict:
    @return:
    """
    date = yaml_dict.get("date")
    today = date.today()
    return date > today

def load_webpage(config, base, path, name, fragments_dict):
    """
    Load a page md file. Also check two special cases:
    * If draft is true, return None so the page is excluded.
    * If publication date is later than today, replace the page content with a "coming soon" message.
    :param base: base path to content area
    :param path: path of this page within the content area
    :param name: name of md file
    :return: A page dictionary, or None if the page should be ignored (eg if draft is true)
    """
    yaml_data, markdown_data = read_webpage_file(base, path, name)

    yaml_dict = parse_yaml(yaml_data, path, name)

    if yaml_dict.get("draft", False):  # If page is draft, return None to indicate it should be ignored.
        return None

    if check_deferred_page(yaml_dict):
        release_date = yaml_dict.get("date")
        markdown_data = f"Coming soon. This article will be released on {release_date}"

    html = convert_markdown_to_html(markdown_data, path, name)

    webpage_dict = create_webpage_dictionary(config, yaml_dict, html, path, name, fragments_dict)
    return webpage_dict

def load_webpages(config, fragments_dict):
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
            if filename.endswith(".md"):
                page = load_webpage(config, base, path, filename, fragments_dict)
                if page:
                    pages.append(page)
    return pages
