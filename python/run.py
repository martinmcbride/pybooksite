# Author:  Martin McBride
# Created: 2022-04-16
# Copyright (c) 2022, Martin McBride
# License: MIT

import config
import webpages
import create_site
import create_site_structure

config = config.load_config()
pages = webpages.load_webpages(config)

html_template = create_site.read_html_template(config)
site_structure = create_site_structure.create_site_structure(pages)
create_site.generate_site(config, html_template, "public", [pages], site_structure)

print(site_structure)
print(config)
print(pages)