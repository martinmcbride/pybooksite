# Author:  Martin McBride
# Created: 2022-04-16
# Copyright (c) 2022, Martin McBride
# License: MIT

import config
import pages
import create_site

config = config.load_config()
pages = pages.load_pages(config)
create_site.copy_site_pages(config, "public")
print(config)
print(pages)