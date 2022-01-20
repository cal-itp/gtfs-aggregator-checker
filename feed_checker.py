from bs4 import BeautifulSoup
from collections import defaultdict
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
import yaml

from cache import get_cached, url_split
from transit_land import get_transit_land_urls
from transitfeeds import get_transitfeeds_urls
from utils import extract_urls


def clean_url(url):
    url = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(url.query, keep_blank_values=True)
    query.pop('api_key', None)
    query.pop('token', None)
    url = url._replace(query=urllib.parse.urlencode(query, True))
    return urllib.parse.urlunparse(url)


def tabulate(columns):
    column_sizes = [max([len(s) for s in column]) for column in columns]
    num_rows = max([len(column) for column in columns])
    for i_row in range(num_rows):
        row = []
        for i_col, column in enumerate(columns):
            value = column[i_row] if len(column) > i_row else ''
            size = column_sizes[i_col]
            row.append(f'{value:<{size}}')
        print('   '.join(row))


def main():
    matched = 0
    domains = {}

    with open('agencies.yml', 'r') as f:
        agencies_obj = yaml.load(f, Loader=yaml.SafeLoader)
    urls = extract_urls(agencies_obj, dict_prefix='gtfs_rt')
    for url in urls:
        url = clean_url(url)
        domain, path = url_split(url)
        if not domain in domains:
            domains[domain] = {
                'in_yml': [],
                'in_feeds': [],
            }
        domains[domain]['in_yml'].append(path)

    # for url in get_transit_land_urls(domains):
    #     domain, path = url_split(clean_url(url))
    #     domains[domain]['in_feeds'].append(path)

    for url in get_transitfeeds_urls(domains):
        domain, path = url_split(clean_url(url))
        domains[domain]['in_feeds'].append(path)

    counts = { 'matched': 0, 'total': 0 }
    for domain in sorted(domains.keys()):
        missing = ['missing']
        matched = ['matched']
        unused = ['unused']
        for path in domains[domain]['in_yml']:
            counts['total'] += 1
            if path in domains[domain]['in_feeds']:
                counts['matched'] += 1
                matched.append(path)
            else:
                missing.append(path)
        for path in domains[domain]['in_feeds']:
            if not path in domains[domain]['in_yml']:
                unused.append(path)
        if len(missing) > 1:
            print(f'\n{domain}')
            tabulate([missing, matched, unused])
    print(f'Matched {counts["matched"]} / {counts["total"]} urls')

if __name__ == '__main__':
    main()
