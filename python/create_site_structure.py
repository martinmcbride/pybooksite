# Author:  Martin McBride
# Created: 2022-04-17
# Copyright (c) 2022, Martin McBride
# License: MIT

from collections import namedtuple

PageItem = namedtuple("PageItem", ["item", "weight", "children"])

def add_books_to_site_structure(webpages, site_structure):
    for webpage in webpages:
        if webpage.get("type", None) == "book":
            if webpage.get("book", None):
                if webpage.get("book", None) not in site_structure:
                    site_structure[webpage["book"]] = PageItem(webpage, webpage.get("weight", 0), dict())
                else:
                    print("More than one book named", webpage.get("book", None))
                    raise Exception()
            else:
                print("Book webpage has no book entry", webpage.get("path", "unknown path"))
                raise Exception()


def add_chapters_to_site_structure(webpages, site_structure):
    for webpage in webpages:
        if webpage.get("type", None) == "chapter":
            if webpage.get("book", None) and webpage.get("chapter", None):
                if webpage.get("book", None) in site_structure:
                    if webpage.get("chapter", None) in site_structure[webpage["book"]].children:
                        print("More than one chapter named", webpage.get("chapter", None))
                        raise Exception()
                    else:
                        site_structure[webpage["book"]].children[webpage["chapter"]] = PageItem(webpage, webpage.get("weight", 0), dict())
                else:
                    print("Chapter references a book that isn't defined", webpage.get("book", None))
                    raise Exception()
            else:
                print("Chapter missing a book or chapter entry", webpage.get("path", "unknown path"))
                raise Exception()


def add_pages_to_site_structure(webpages, site_structure):
    for webpage in webpages:
        if webpage.get("type", None) == "page":
            if webpage.get("book", None) and webpage.get("chapter", None):
                if webpage.get("book", None) in site_structure and webpage.get("chapter", None) in site_structure[webpage["book"]].children:
                    site_structure[webpage["book"]].children[webpage["chapter"]].children[webpage["title"]] = PageItem(webpage, webpage.get("weight", 0), None)
                else:
                    print("Page references a book or chapter that isn't defined", webpage.get("book", None))
                    raise Exception()
            else:
                print("Page missing a book or chapter entry", webpage.get("path", "unknown path"))
                raise Exception()

def dump_site_structure(site_structure):
    for book, book_content in site_structure.items():
        print(book)
        for chapter, chapter_content in book_content.children.items():
            print(" ", chapter)
            for page, page_content in chapter_content.children.items():
                print("   ", page)

def create_site_structure(webpages):
    site_structure = dict()
    add_books_to_site_structure(webpages, site_structure)
    add_chapters_to_site_structure(webpages, site_structure)
    add_pages_to_site_structure(webpages, site_structure)
    return site_structure

def get_toc_for_webpage(site_structure, webpage):
    toc = []
    book = webpage.get("book", None)
    if not book:
        return toc

    book_content = site_structure[book]
    for chapter, chapter_content in sorted(book_content.children.items(), key=lambda x: x[1].weight):
        toc.append(dict(style="chapter_toc", title=chapter_content.item.get("title", ""), link="/" + chapter_content.item.get("path", "")))
        for page, page_content in sorted(chapter_content.children.items(), key=lambda x: x[1].weight):
            toc.append(dict(style="page_toc", title=page_content.item.get("title", ""), link="/" + page_content.item.get("path", "")))

    return toc

