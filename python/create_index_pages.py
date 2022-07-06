# Author:  Martin McBride
# Created: 2022-04-21
# Copyright (c) 2022, Martin McBride
# License: MIT

month_names = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec', ]

def get_month_year(date):
    month = int(date[5:7]) - 1
    return month_names[month] + ' ' + date[0:4]

def create_recent_pages_page(webpages):
    entries = []
    for webpage in webpages:
        entries.append((webpage["title"], webpage["path"], str(webpage.get("date", ""))))
    entries.sort(key=lambda x: x[2], reverse=True)
    entries = entries[:50]
    title = 'Most recent ' + str(len(entries)) + ' articles'

    content = ''
    month = '0000-00'
    first = True
    if entries:
        for t, p, d in entries:
            new = month[:7]!=d[:7]
            if new:
                month = d[:8]
                if not first:
                    content += '</ol>'
                first = False
                content += '<h3>' + get_month_year(month) + '</h3>'
                content += '<ol class="list-unstyled">'
            content += '<li><a href="' + p + '">' + t + '</a></li>'
    content += '</ol>'

    recentpage = dict(title=title, content=content, tags=[], categories=[], path="/recent/")
    return recentpage

def create_all_pages_page(webpages):
    entries = []
    for webpage in webpages:
        entries.append((webpage["title"], webpage["path"]))
    entries.sort(key=lambda x: x[0])

    title = 'All articles (' + str(len(entries)) + ')'

    content = ''
    alphabet = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'
    for initial in alphabet:
        initial_entries = [e for e in entries if e[0][0].upper()==initial]
        if initial_entries:
            content += '<p><h3>' + initial + '</h3>'
            content += '<ol class="list-unstyled">'
            for t, p in initial_entries:
                content += '<li><a href="' + p + '">' + t + '</a></li>'
            content += '</ol>'

    initial_entries = [e for e in entries if e[0][0].upper() not in alphabet]
    if initial_entries:
        content += '<p><h3>Other</h3>'
        content += '<ol class="list-unstyled">'
        for t, p in initial_entries:
            content += '<li><a href="' + p + '">' + t + '</a></li>'
        content += '</ol>'

    indexpage = dict(title=title, content=content, tags=[], categories=[], path="/all/")
    return indexpage

def create_index_pages(webpages):
    return [create_all_pages_page(webpages),
            create_recent_pages_page(webpages),
            ]