# Author:  Martin McBride
# Created: 2022-04-24
# Copyright (c) 2022, Martin McBride
# License: MIT
import logging
import os.path
import page_utils

def create_site_map(webpages, public_path, site_url):
    """
    Create a sitemap and write it to teh top level of the public area.

    A site map is an XML file listing every page on the site, including the URL, title, and date of last update.
    :param webpages: List of pages
    :param public_path: Path to public area
    :param site_url: Main site URL
    :return: None
    """
    entries = []
    for webpage in webpages:
        entries.append((webpage["title"], page_utils.get_page_full_url(webpage, site_url), webpage.get("date", None)))
    entries.sort(key=lambda x: x[0])
    xml_content = """<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">"""

    for title, path, date in entries:
        xml_content += "\n  <url>"
        xml_content += "".join(("\n    <loc>", path, "</loc>"))
        if date:
            xml_content += "\n    <lastmod>" + str(date) + "</lastmod>"
        xml_content += "\n  </url>"

    xml_content += "\n</urlset>"

    try:
        with open(os.path.join(public_path, "sitemap.xml"), "w") as outfile:
            outfile.write(xml_content)
    except Exception as e:
        logging.error("Error writing sitemap.xml")
        logging.error(e)
        raise

