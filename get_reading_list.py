# !/usr/bin/env python3
"""This module imports each item from my Safari readinglist into an Airtable base.
Aftwerwards, I manually remove all links from the readinglist.
Ideally, the code is run a couple times a week. From the command line, it's:
python3 ~/code/reading_list/get_reading_list.py
"""
import os
import plistlib
import time
from airtable import Airtable

airtab = Airtable(os.environ['articles_db'], 'links', os.environ['AIRTABLE_API_KEY'])
airtab_log = Airtable(os.environ['log_db'], 'log', os.environ['AIRTABLE_API_KEY'])
input_file = os.path.join(os.environ['HOME'], 'Library/Safari/Bookmarks.plist')


def wrap_it_up(t0, new, total=None, function=None):
    this_dict = {'module': 'get_reading_list.py'}
    this_dict['function'] = function
    this_dict['duration'] = round(time.time() - t0, 2)
    this_dict['total'] = total
    this_dict['new'] = new
    airtab_log.insert(this_dict, typecast=True)


def get_reading_list():
    new_links, t0 = 0, time.time()
    with open(input_file, 'rb') as plist_file:
        plist = plistlib.load(plist_file)
    children = plist['Children']
    for child in children:
        if child.get('Title', None) == 'com.apple.ReadingList':
            reading_list = child
    bookmarks = reading_list['Children']
    print("total links on reading list: " + str(len(bookmarks)))
    for bookmark in bookmarks:
        link = bookmark['URLString']
        search_results = airtab.search('url', link)
        if not search_results:
            this_dict = {}
            this_dict['url'] = link
            this_dict['via'] = 'get_reading_list.py'
            airtab.insert(this_dict)
            new_links += 1
    wrap_it_up(t0, new_links, len(bookmarks), 'get_reading_list')


def main():
    get_reading_list()


if __name__ == "__main__":
    main()
