#!/usr/bin/env python
"""This module provides a function for shipping logs to Airtable."""
import os
import time
from airtable import Airtable
import cloudinary
from documentcloud import DocumentCloud

airtab_articles = Airtable(os.environ['articles_db'], 'links', os.environ['AIRTABLE_API_KEY'])

airtab_log = Airtable(os.environ['log_db'], 'log', os.environ['AIRTABLE_API_KEY'])

dc = DocumentCloud(username=os.environ['MUCKROCK_USERNAME'],
                   password=os.environ['MUCKROCK_PW'])

cloudinary.config(cloud_name='bfeldman89',
                  api_key=os.environ['CLOUDINARY_API_KEY'],
                  api_secret=os.environ['CLOUDINARY_API_SECRET'])

muh_headers = {
    'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_6) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36'}


my_funcs = {'get_reading_list': 'rec43zeXFYciU2ZUH',
            'clean_urls': 'rec6YZFb0DMukAXLv',
            'extract_kwds': 'recdrZbvp7pWvI4qK',
            'scrape_pages': 'recJJ2UyT9QWCPLh4',
            'upload_img': 'recjZTLZAMT1qrihh'}


def wrap_from_module(module):
    def wrap_it_up(t0, new=None, total=None, function=None):
        this_dict = {
            'module': module,
            'function': function,
            '_function': my_funcs[function],
            'duration': round(time.time() - t0, 2),
            'total': total,
            'new': new
        }
        airtab_log.insert(this_dict, typecast=True)

    return wrap_it_up
