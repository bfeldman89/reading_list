# !/usr/bin/env python3
"""This module does blah blah."""
import datetime
import time
import urllib.parse
import os
import requests

from airtable import Airtable
from gensim.summarization import keywords as gen_kwds
from newspaper import Article
from newspaper.article import ArticleException

airtab = Airtable(os.environ['articles_db'],
                  'links', os.environ['AIRTABLE_API_KEY'])


def scrape_pages():
    records = airtab.get_all(view='needs news_scraper.py')
    for record in records:
        this_dict = {}
        url = record['fields']['clean url']
        this_dict['script ran'] = time.strftime('%c')
        try:
            article = Article(url)
            article.download()
            article.parse()
            this_dict['author2'] = ', '.join(article.authors)
            this_dict['body2'] = article.text
            article.nlp()
            this_dict['kwds2'] = ', '.join(article.keywords)
            this_dict['excerpt2'] = article.summary
        except ArticleException as err:
            print(f"🤬: {err}")
            this_dict['oops'] = 'newspaper fucked up'
        finally:
            airtab.update(record['id'], this_dict)
    return len(records)


def extract_kwds():
    records = airtab.get_all(view='needs kwds3', fields=[
        'title', 'body2', 'clean title'])
    for record in records:
        this_dict = {}
        if 'clean title' in record['fields']:
            data = record['fields']['clean title'] + \
                '\n' + record['fields']['body2']
        else:
            data = record['fields']['body2']
        this_dict['kwds3'] = ', '.join(
            gen_kwds(data, words=15, split=True, lemmatize=True))
        airtab.update(record['id'], this_dict)


def clean_urls():
    records = airtab.get_all(view='needs parsing', fields='clean url')
    for record in records:
        x = urllib.parse.urlparse(record['fields']['clean url'])
        this_dict = {}
        this_dict['parsed_at'] = datetime.datetime.utcnow().replace(
            tzinfo=datetime.timezone.utc).strftime('%Y-%m-%d %H:%M')
        this_dict['scheme'] = x.scheme
        this_dict['params'] = x.params
        this_dict['query'] = x.query
        this_dict['netloc'] = x.netloc
        this_dict['path'] = x.path
        airtab.update(record['id'], this_dict)


def upload_img():
    records = airtab.get_all(view='needs image', fields='img_url')
    for record in records:
        this_dict = {'img': [{'url': record['fields']['img_url']}]}
        airtab.update(record['id'], this_dict)


def main():
    t0 = time.time()
    scrape_pages()
    extract_kwds()
    clean_urls()
    upload_img()
    data = {'Value1': 'muh_news.py'}
    data['Value2'] = round(time.time() - t0, 2)
    ifttt_event_url = os.environ['IFTTT_WEBHOOKS_URL'].format('muh_news')
    requests.post(ifttt_event_url, json=data)


if __name__ == "__main__":
    main()
