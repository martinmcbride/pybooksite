# Author:  Martin McBride
# Created: 2022-04-21
# Copyright (c) 2022, Martin McBride
# License: MIT

def create_tag_linkname(tag):
    return 'tag-' + tag.replace(' ', '-')

def create_tag_link(tag):
    return 'tags/' + create_tag_linkname(tag) + '/'

def create_tag_page(tag, webpages):
    title = 'Tag: ' + tag
    path = create_tag_link(tag)

    entries = []
    for webpage in webpages:
        if tag in webpage.get("tags", []):
            entries.append((webpage["title"], '/' + webpage["path"]))
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

    tagpage = dict(title=title, content=content, tags=[], categories=[], path="tags/")
    return tagpage

def create_all_tags(webpages):
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
