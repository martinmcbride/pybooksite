# Author:  Martin McBride
# Created: 2022-07-05
# Copyright (c) 2022, Martin McBride
# License: MIT

import os.path

def get_webpage_path(filepath, filename):
    """
    Get the HTML path of the page
    :param filepath: Path to file
    :param filename: Name of file
    :return: HTML path
    """
    # Each html file is renamed to index.html and stored in its own directory, so the full path is formed by joining the
    # path and the name. The exception is for files that are named index - they are stored in the original folder.
    #print("**", filepath, filename)
    name = os.path.splitext(filename)[0]
    #print("++", filepath, name)
    if name!='index':
        if filepath:
            filepath = "/" + filepath + "/" + name + "/"
        else:
            filepath = "/" + name  + "/" # Top level items such as about.md have no path, so create about/index.html
    else:
        if filepath:
            filepath = "/" + filepath + "/"
        else:
            filepath = "/"
    return filepath



def get_page_full_url(webpage, site_url):
    """
    Create a full url for a web page, eg https://www.example.com/folder/page/
    :param webpage: Web page dictionary
    :param site_url: Base URL of site
    :return:
    """
    return site_url + webpage["path"]