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

def create_tag_cloud(pages):

    sizes = ['85', '85', '85', '95', '105', '115', '125', '135', '145', '155']

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
            pc = sizes[min(size,9)]
            tags.append('<a href="' + link + '"><span style="font-size:' + pc + '%;">' + tag + '</span></a>')

    tagcloud = ' '.join(tags)
    return tagcloud