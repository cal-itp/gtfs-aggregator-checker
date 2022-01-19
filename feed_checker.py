from bs4 import BeautifulSoup
from collections import defaultdict
import json
import os
import sys
import urllib.error
import urllib.parse
import urllib.request
import yaml

from cache import get_cached
from transit_land import get_transit_land_feed, get_transit_land_feeds


def clean_url(url):
    url = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(url.query, keep_blank_values=True)
    query.pop('api_key', None)
    query.pop('token', None)
    url = url._replace(query=urllib.parse.urlencode(query, True))
    return urllib.parse.urlunparse(url)


def url_split(url):
    # For analyzing urls we usually only want the domain and the path+query
    url_obj = urllib.parse.urlparse(url)
    if url_obj.query:
        return url_obj.netloc, f'{url_obj.path}?{url_obj.query}'
    return url_obj.netloc, url_obj.path


def extract_urls(dict_or_list, dict_prefix=''):
    """
    Recurse obj and return any urls
    """
    urls = []
    def match(key, value):
        return isinstance(value, (dict, list)) or key.startswith(dict_prefix)
    def extract(obj):
        if isinstance(obj, dict):
            obj = [value for key, value in obj.items() if match(key, value)]
        if isinstance(obj, str):
            if obj.startswith('http'):
                urls.append(obj)
        elif isinstance(obj, list):
            [extract(i) for i in obj]

    extract(dict_or_list)
    return urls


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
    content = get_transit_land_feeds(0, 10000)
    result = json.loads(content)
    onestop_ids = [e['onestop_id'] for e in result['data']['entities']]

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

    # TODO reading/parsing these files is slow. Move to transit_land.py and cache
    for onestop_id in onestop_ids:
        html = get_cached(
            onestop_id,
            lambda: get_transit_land_feed(onestop_id),
            directory='.cache/transit_land'
        )
        soup = BeautifulSoup(html, 'html.parser')
        for tag in soup.find_all('code'):
            url = tag.text
            url = clean_url(tag.text)
            domain, path = url_split(url)
            if domain in domains:
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
