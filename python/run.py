# Author:  Martin McBride
# Created: 2022-04-16
# Copyright (c) 2022, Martin McBride
# License: MIT

import config
import webpages
import create_site
import create_site_structure
import tag_pages
import category_pages
import create_index_pages
import fragments

config = config.load_config()
fragments_dict = fragments.get_fragments(config)
fragments.replace_fragments(fragments_dict, config)
webpages = webpages.load_webpages(config, fragments_dict)

html_template = create_site.read_html_template(config)
site_structure = create_site_structure.create_site_structure(webpages)
tagpages = tag_pages.create_all_tags(webpages)
tagcloud = tag_pages.create_tag_cloud(webpages)
categorypages = category_pages.create_all_categories(webpages)
indexpages = create_index_pages.create_index_pages(webpages)
create_site.generate_site(config, html_template, config["public"], [webpages, tagpages, categorypages, indexpages],
                          site_structure, config["site-url"], tagcloud)