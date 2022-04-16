# Author:  Martin McBride
# Created: 2022-04-16
# Copyright (c) 2022, Martin McBride
# License: MIT

import shutil, os
import pystache

def create_url(base, page):
    directory = os.path.join(base, page.path)
    html_name = 'index.html'
    html_path = os.path.join(directory, html_name)
    return directory, html_path

def read_template(config):
    try:
        with open(config["template"]) as infile:
            template = ''.join(infile)
    except Exception as e:
        print("Error reading template file", config["template"])
        print(e)
        raise

    return template


def write_page(config, template, public_path, page, pages):

    html = pystache.render(template, page)

    directory, html_path = create_url(public_path, page["path"])
    try:
        os.makedirs(directory, exist_ok=True)
        with open(html_path, 'w') as outfile:
            outfile.write(html)
    except Exception as e:
        print("Error writing outout file", html_path)
        print(e)
        raise



def write_site_pages(config, public_path, pages_list):

    try:
        shutil.rmtree(public_path, ignore_errors=False, onerror=None)
    except Exception as e:
        print("Failed to delete public area", public_path)
        print(e)
        raise

    for pages in pages_list:
        for page in pages:
            write_page(config, public_path, page, pages)

