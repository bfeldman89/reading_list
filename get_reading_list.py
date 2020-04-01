#!/usr/bin/env python
"""This module imports each item from my Safari readinglist into an Airtable base.
Aftwerwards, I manually remove all links from the readinglist.
Ideally, the code is run a couple times a week. From the command line, it's:
python3 ~/code/reading_list/get_reading_list.py
"""
import os
import plistlib
import time
from common import airtab_articles as airtab, wrap_from_module

wrap_it_up = wrap_from_module('reading_list/get_reading_list.py')

input_file = os.path.join(os.environ['HOME'], 'Library/Safari/Bookmarks.plist')

t0 = time.time()


def get_reading_list():
    with open(input_file, 'rb') as plist_file:
        plist = plistlib.load(plist_file)
    children = plist['Children']
    for child in children:
        if child.get('Title', None) == 'com.apple.ReadingList':
            bookmarks = child.get('Children')
            return bookmarks


def parse_reading_list(bookmarks):
    new_links = 0
    if bookmarks:
        total_links = len(bookmarks)
        for bookmark in bookmarks:
            this_dict = {}
            this_dict['url'] = bookmark.get('URLString')
            res = airtab.search('url', this_dict['url'])
            if not res:
                this_dict['via'] = 'get_reading_list.py'
                this_dict['title'] = bookmark.get('URIDictionary')['title']
                try:
                    this_dict['excerpt'] = bookmark.get('ReadingList')['PreviewText']
                except KeyError as err:
                    print(err)
                this_dict['img_url'] = bookmark.get('imageURL')
                airtab.insert(this_dict)
                new_links += 1
    else:
        total_links = 0
    wrap_it_up(t0, new_links, total_links, 'get_reading_list')


def main():
    this_list = get_reading_list()
    parse_reading_list(this_list)


if __name__ == "__main__":
    main()
