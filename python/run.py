# Author:  Martin McBride
# Created: 2022-04-16
# Copyright (c) 2022, Martin McBride
# License: MIT

import config
import pages
import create_site

config = config.load_config()
pages = pages.load_pages(config)

html_template = create_site.read_html_template(config)
create_site.write_site_pages(config, html_template, "public", [pages])
print(config)
print(pages)