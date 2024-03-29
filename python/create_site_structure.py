# Author:  Martin McBride
# Created: 2022-04-17
# Copyright (c) 2022, Martin McBride
# License: MIT
import logging
from collections import namedtuple

PageItem = namedtuple("PageItem", ["item", "weight", "children"])

month_names = ["", "Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

def month_name(month):
    if month < 1 or month > 12:
        logging.error("Invalid month ", month)
        raise Exception()
    return month_names[month]

def is_book_page(webpage):
    """
    Check is webpage is part of a book
    :param webpage:
    :return:
    """
    book = webpage.get("book", None)
    return bool(book)


def is_blog_page(webpage):
    """
    Check is webpage is part of the blog
    :param webpage:
    :return:
    """
    return webpage.get("type", None) == "post"


def get_toc_title_for_webpage(site_structure, webpage):
    """
    Find the title of the book associated with a page.
    :param site_structure:
    :param webpage:
    :return: shorttitle, style, path or None if not a book
    """
    if is_book_page(webpage):
        book = webpage.get("book", None)
        book_item = site_structure[book].item
        shorttitle = book_item.get("shorttitle", None)
        path = book_item.get("path")
        style = "toc-title-current" if webpage is book_item else "toc-title"
        return shorttitle, style, path if shorttitle and path else None

    if is_blog_page(webpage):
        return "Posts", "toc-title", "/blog/"

    return None

def add_books_to_site_structure(webpages, site_structure):
    for webpage in webpages:
        if webpage.get("type", None) == "book":
            if webpage.get("book", None):
                if webpage.get("book", None) not in site_structure:
                    site_structure[webpage["book"]] = PageItem(webpage, webpage.get("weight", 0), dict())
                else:
                    logging.error("More than one book named", webpage.get("book", None))
                    raise Exception()
            else:
                logging.error("Book webpage has no book entry", webpage.get("path", "unknown path"))
                raise Exception()


def add_chapters_to_site_structure(webpages, site_structure):
    for webpage in webpages:
        if webpage.get("type", None) == "chapter":
            if webpage.get("book", None) and webpage.get("chapter", None):
                if webpage.get("book", None) in site_structure:
                    if webpage.get("chapter", None) in site_structure[webpage["book"]].children:
                        logging.error("More than one chapter named", webpage.get("chapter", None))
                        raise Exception()
                    else:
                        site_structure[webpage["book"]].children[webpage["chapter"]] = PageItem(webpage, webpage.get("weight", 0), dict())
                else:
                    logging.error("Chapter references a book that isn't defined", webpage.get("book", None))
                    raise Exception()
            else:
                logging.error("Chapter missing a book or chapter entry", webpage.get("path", "unknown path"))
                raise Exception()


def add_pages_to_site_structure(webpages, site_structure):
    for webpage in webpages:
        if webpage.get("type", None) == "page":
            if webpage.get("book", None) and webpage.get("chapter", None):
                if webpage.get("book", None) in site_structure and webpage.get("chapter", None) in site_structure[webpage["book"]].children:
                    site_structure[webpage["book"]].children[webpage["chapter"]].children[webpage["title"]] = PageItem(webpage, webpage.get("weight", 0), None)
                else:
                    logging.error("Page references a book or chapter that isn't defined", webpage.get("book", None), webpage.get("chapter", None), webpage.get("title", None))
                    raise Exception()
            else:
                logging.error("Page missing a book or chapter entry", webpage.get("path", "unknown path"))
                raise Exception()

def add_posts_to_site_structure(webpages, site_structure):
    site_structure["posts"] = []
    for webpage in webpages:
        if webpage.get("type", None) == "post":
            if not webpage.get("date", None):
                logging.error("Page of type post has no date", webpage.get("path", "unknown path"))
                raise Exception()
            site_structure["posts"].append(PageItem(webpage, webpage.get("weight", 0), dict()))


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
    add_posts_to_site_structure(webpages, site_structure)
    return site_structure


def get_toc_for_bookpage(site_structure, webpage):
    toc = []
    book = webpage.get("book", None)
    current_chapter = webpage.get("chapter", None)

    book_content = site_structure[book]
    for chapter, chapter_content in sorted(book_content.children.items(), key=lambda x: x[1].weight):
        style = "chapter-toc-current" if webpage is chapter_content.item else "chapter-toc"
        toc.append(dict(style=style, title=chapter_content.item.get("shorttitle", ""),
                        link=chapter_content.item.get("path", "")))
        for page, page_content in sorted(chapter_content.children.items(), key=lambda x: x[1].weight):
            if current_chapter and page_content.item.get("chapter", None) == current_chapter:
                style = "page-toc-current" if webpage is page_content.item else "page-toc"
                toc.append(dict(style=style, title=page_content.item.get("shorttitle", ""),
                                link=page_content.item.get("path", "")))
    return toc


def get_toc_for_blogpage(site_structure, webpage):
    toc = []
    current_year = 3000
    current_month = 13
    page_year = webpage.get("date").year
    page_month = webpage.get("date").month

    blog_content = site_structure["posts"]
    for post in reversed(sorted(blog_content, key=lambda x: x.item.get("date", ""))):
        new_year = post.item.get("date").year
        new_month = post.item.get("date").month
        if new_year != current_year:
            style = "chapter-toc-current" if new_year == page_year else "chapter-toc"
            toc.append(dict(style=style, title=new_year,
                        link=post.item.get("path", "")))
            current_month = 13
        if new_month != current_month and new_year == page_year:
            style = "chapter-toc-current" if new_month == page_month else "chapter-toc"
            toc.append(dict(style=style, title=month_name(new_month),
                        link=post.item.get("path", "")))
        if new_month == page_month and new_year == page_year:
            style = "page-toc-current" if webpage is post.item else "page-toc"
            toc.append(dict(style=style, title=post.item.get("shorttitle", ""),
                            link=post.item.get("path", "")))
        current_year = new_year
        current_month = new_month
    return toc


def get_toc_for_webpage(site_structure, webpage):
    if is_book_page(webpage):
        return get_toc_for_bookpage(site_structure, webpage)

    if is_blog_page(webpage):
        return get_toc_for_blogpage(site_structure, webpage)

    return []

def get_book_pages_for_webpage(site_structure, webpage):
    pages = []
    current_index = -1
    book = webpage.get("book", None)
    if not is_book_page(webpage):
        return current_index, pages

    book_content = site_structure[book]
    page_index = 0
    for chapter, chapter_content in sorted(book_content.children.items(), key=lambda x: x[1].weight):
        if webpage is chapter_content.item:
            current_index = page_index
        pages.append(chapter_content.item.get("path", ""))
        page_index += 1
        for page, page_content in sorted(chapter_content.children.items(), key=lambda x: x[1].weight):
            if webpage is page_content.item:
                current_index = page_index
            pages.append(page_content.item.get("path", ""))
            page_index += 1

    return current_index, pages

def get_related_pages_for_webpage(site_structure, webpage):
    related_pages = []
    book = webpage.get("book", None)
    current_chapter = webpage.get("chapter", None)
    if not book:
        return related_pages

    book_content = site_structure[book]

    if webpage.get("type", None) == "book":
        for chapter, chapter_content in sorted(book_content.children.items(), key=lambda x: x[1].weight):
            related_pages.append(dict(title=chapter_content.item.get("title", ""),
                                      link=chapter_content.item.get("path", "")))
    else:
        for chapter, chapter_content in sorted(book_content.children.items(), key=lambda x: x[1].weight):
            if chapter == current_chapter:
                for page, page_content in sorted(chapter_content.children.items(), key=lambda x: x[1].weight):
                    if webpage is not page_content.item:
                        related_pages.append(dict(title=page_content.item.get("title", ""),
                                      link=page_content.item.get("path", "")))
    return related_pages

