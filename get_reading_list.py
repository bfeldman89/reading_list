# !/usr/bin/env python3
"""This module does blah blah."""
import os
import plistlib
import time
import requests
from airtable import Airtable

airtab = Airtable(os.environ['articles_db'], 'ifttt',
                  os.environ['AIRTABLE_API_KEY'])
input_file = os.path.join(
    os.environ['HOME'], 'Library/Safari/Bookmarks.plist')
t0 = time.time()


def get_it():
    # set airtab for the "ifttt" table in the "ARTICLES" base
    old_links, new_links = 0, 0
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
        else:
            old_links += 1
    results = f"new links: {new_links}\nold links: {old_links}\
               \nduration: {round(time.time() - t0, 2)}"
    return results


def main():
    data = {'Value1': 'get_reading_list.py'}
    data['Value2'] = get_it()
    data['Value3'] = 'success'
    ifttt_event_url = os.environ['IFTTT_WEBHOOKS_URL'].format('code_completed')
    requests.post(ifttt_event_url, json=data)


if __name__ == "__main__":
    main()
