# Author:  Martin McBride
# Created: 2022-04-24
# Copyright (c) 2022, Martin McBride
# License: MIT

import os.path
import page_utils

def create_site_map(webpages, public_path, site_url):
    entries = []
    for webpage in webpages:
        entries.append((webpage["title"], page_utils.get_page_full_url(webpage, site_url), webpage.get("date", None)))
        print(site_url, webpage["path"])
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
        print("Error writing sitemap.xml")
        print(e)
        raise

