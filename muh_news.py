# !/usr/bin/env python3
"""This module does blah blah."""
import datetime
import time
import urllib.parse

from gensim.summarization import keywords as gen_kwds
from newspaper import Article
from newspaper.article import ArticleException

from common import airtab_articles as airtab, wrap_from_module


wrap_it_up = wrap_from_module('muh_news.py')


def scrape_pages():
    t0, i = time.time(), 0
    # records = airtab.get_all(view='needs news_scraper.py')
    records = airtab.get_all(formula='script ran = ""')
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
            i += 1
        except ArticleException as err:
            print(f"🤬: {err}")
            this_dict['oops'] = 'newspaper fucked up'
        finally:
            airtab.update(record['id'], this_dict)
    wrap_it_up(t0=t0, new=i, total=len(records), function='scrape_pages')


def extract_kwds():
    t0 = time.time()
    records = airtab.get_all(view='needs kwds3', fields=['title', 'body2', 'clean title'], max='100')
    for record in records:
        this_dict = {}
        if 'clean title' in record['fields']:
            data = record['fields']['clean title'] + \
                '\n' + record['fields']['body2']
        else:
            data = record['fields']['body2']
        this_dict['kwds3'] = ', '.join(gen_kwds(data, words=15, split=True, lemmatize=True))
        airtab.update(record['id'], this_dict)
    wrap_it_up(t0=t0, new=len(records), total=len(records), function='extract_kwds')


def clean_urls():
    t0 = time.time()
    records = airtab.search('parsed_at', '', fields='clean url')
    # records = airtab.get_all(view='needs parsing', fields='clean url')
    for record in records:
        x = urllib.parse.urlparse(record['fields']['clean url'])
        this_dict = {}
        this_dict['parsed_at'] = datetime.datetime.utcnow().replace(tzinfo=datetime.timezone.utc).strftime('%Y-%m-%d %H:%M')
        this_dict['scheme'] = x.scheme
        this_dict['params'] = x.params
        this_dict['query'] = x.query
        this_dict['netloc'] = x.netloc
        this_dict['path'] = x.path
        airtab.update(record['id'], this_dict)
    wrap_it_up(t0=t0, new=len(records), total=len(records), function='clean_urls')


def upload_img():
    t0 = time.time()
    records = airtab.get_all(formula="AND(img_url != '', img = '')", fields='img_url')
    # records = airtab.get_all(view='needs image', fields='img_url')
    for record in records:
        this_dict = {'img': [{'url': record['fields']['img_url']}]}
        airtab.update(record['id'], this_dict)
    wrap_it_up(t0=t0, new=len(records), total=len(records), function='upload_img')


def main():
    scrape_pages()
    extract_kwds()
    clean_urls()
    upload_img()


if __name__ == "__main__":
    main()
