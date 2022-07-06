# Author:  Martin McBride
# Created: 2022-04-21
# Copyright (c) 2022, Martin McBride
# License: MIT

def create_category_linkname(category):
    return 'category-' + category.replace(' ', '-')

def create_category_link(category):
    return '/categories/' + create_category_linkname(category) + '/'

def create_category_page(category, webpages):
    """
    Create a page for a particular category
    :param category: Category name
    :param webpages: Webpages list
    :return: the page
    """
    title = 'Category: ' + category
    path = create_category_link(category)

    entries = []
    for webpage in webpages:
        if category in webpage.get("categories", []):
            entries.append((webpage["title"], webpage["path"]))
    entries.sort(key=lambda x: x[0])

    content = ''
    if entries:
        content += '<ol class="list-unstyled">'
        for t, p in entries:
            content += '<li><a href="' + p + '">' + t + '</a></li>'
        content += '</ol>'

    categorypage = dict(title=title, content=content, tags=[], categories=[], path=path)

    return categorypage

def create_allcategory_page(webpages):
    """
    Create a page listing all categories
    :param webpages:
    :return: the page
    """

    entry_set = set()
    for webpage in webpages:
        for category in webpage.get("categories", []):
            entry_set.add((category, "/" + create_category_link(category)))

    entries = list(entry_set)
    entries.sort(key=lambda x: x[0])
    title = 'All categories (' + str(len(entries)) + ')'

    content = ''
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for initial in alphabet:
        initial_entries = [e for e in entries if e[0][0].upper()==initial]
        if initial_entries:
            content += '<p><h3>' + initial + '</h3> '
            content += ', '.join(['<a href="' + p + '">' + t + '</a>' for t, p in initial_entries])

    initial_entries = [e for e in entries if e[0][0].upper() not in alphabet]
    if initial_entries:
        content += '<p><h3>Other</h3>'
        content += ', '.join(['<a href="' + p + '">' + t + '</a>' for t, p in initial_entries])

    categorypage = dict(title=title, content=content, tags=[], categories=[], path="/categories/")
    return categorypage

def create_all_categories(webpages):
    """
    Create all the required category pages. That includes a page for every individual category and the all categories
    page.
    :param webpages:
    :return: The list of pages
    """
    categories = set()
    for webpage in webpages:
        for category in webpage.get("categories", []):
            categories.add(category)

    categorypages = []
    for category in categories:
        categorypages.append(create_category_page(category, webpages))

    allcategories = create_allcategory_page(webpages)
    categorypages.append(allcategories)

    return categorypages
