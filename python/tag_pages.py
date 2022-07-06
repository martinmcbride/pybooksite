# Author:  Martin McBride
# Created: 2022-04-21
# Copyright (c) 2022, Martin McBride
# License: MIT

def create_tag_linkname(tag):
    return 'tag-' + tag.replace(' ', '-')

def create_tag_link(tag):
    return '/tags/' + create_tag_linkname(tag) + '/'

def create_tag_page(tag, webpages):
    """
    Create a page for a particular tag
    :param tag: Tag name
    :param webpages: Webpages list
    :return: the page
    """
    title = 'Tag: ' + tag
    path = create_tag_link(tag)

    entries = []
    for webpage in webpages:
        if tag in webpage.get("tags", []):
            entries.append((webpage["title"], webpage["path"]))
    entries.sort(key=lambda x: x[0])

    content = ''
    if entries:
        content += '<ol class="list-unstyled">'
        for t, p in entries:
            content += '<li><a href="' + p + '">' + t + '</a></li>'
        content += '</ol>'

    tagpage = dict(title=title, content=content, tags=[], categories=[], path=path)

    return tagpage

def create_alltag_page(webpages):
    """
    Create a page listing all tags
    :param webpages:
    :return: the page
    """

    entry_set = set()
    for webpage in webpages:
        for tag in webpage.get("tags", []):
            entry_set.add((tag, "/" + create_tag_link(tag)))

    entries = list(entry_set)
    entries.sort(key=lambda x: x[0])
    title = 'All tags (' + str(len(entries)) + ')'

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

    tagpage = dict(title=title, content=content, tags=[], categories=[], path="/tags/")
    return tagpage

def create_all_tags(webpages):
    """
    Create all the required tag pages. That includes a page for every individual tag and the all tags
    page.
    :param webpages:
    :return: The list of pages
    """
    tags = set()
    for webpage in webpages:
        for tag in webpage.get("tags", []):
            tags.add(tag)

    tagpages = []
    for tag in tags:
        tagpages.append(create_tag_page(tag, webpages))

    alltags = create_alltag_page(webpages)
    tagpages.append(alltags)

    return tagpages

def create_tag_cloud(pages):

    sizes = ['tagcloud0',
             'tagcloud1',
             'tagcloud2',
             'tagcloud3',
             'tagcloud4',
             'tagcloud5',
             'tagcloud6',
             'tagcloud7',
             'tagcloud8',
             'tagcloud9',
             ]

    entry_set = set()
    entry_count = dict()
    for page in pages:
        for tag in page.get("tags", []):
            entry_set.add((tag, create_tag_link(tag)))
            if tag in entry_count:
                entry_count[tag] += 1
            else:
                entry_count[tag] = 1

    entries = list(entry_set)
    entries.sort(key=lambda x: x[0])

    tags = []
    for tag, link in entries:
        size = entry_count[tag]
        if size > 1:
            tag_style = sizes[min(size,9)]
            tags.append('<a href="' + link + '"><span class="' + tag_style + '">' + tag + '</span></a>')

    tagcloud = ' '.join(tags)
    return tagcloud