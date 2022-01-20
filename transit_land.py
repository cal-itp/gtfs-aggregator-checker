from bs4 import BeautifulSoup
import json
import urllib.parse
import urllib.request

from cache import get_cached
from utils import url_split


def _get_transit_land_feeds(after, limit):
    req = urllib.request.Request('https://demo.transit.land/api/v2/query', { 'method': 'POST' })

    req.add_header('Content-Type', 'application/json') # 400 without this
    req.add_header('referer', 'https://www.transit.land/') # 403 without this

    payload = {
        "operationName": None,
        "variables": {
            "search": None,
            "limit": limit,
            "specs": ["gtfs", "gtfs-rt", "gbfs", "mds"],
            "fetch_error": None,
            "import_status": None,
            "tags": {},
            "after": after
        },
        "query": """query ($specs: [String!], $after: Int, $limit: Int, $search: String, $fetch_error: Boolean, $import_status: ImportStatus, $tags: Tags) {
      entities: feeds(
        after: $after
        limit: $limit
        where: {search: $search, spec: $specs, fetch_error: $fetch_error, import_status: $import_status, tags: $tags}
      ) {
        id
        onestop_id
        spec
        tags
        feed_state {
          id
          feed_version {
            id
            fetched_at
            sha1
            feed_version_gtfs_import {
              id
              created_at
              __typename
            }
            __typename
          }
          last_fetch_error
          last_fetched_at
          last_successful_fetch_at
          __typename
        }
        __typename
      }
    }"""
    }

    data = json.dumps(payload)

    r = urllib.request.urlopen(req, data=data.encode())
    return r.read().decode()


def get_transit_land_feed(onestop_id):
    slug = urllib.parse.quote(onestop_id)
    req = urllib.request.Request(f'https://www.transit.land/feeds/{slug}')
    r = urllib.request.urlopen(req)
    return r.read().decode()


def get_transit_land_feeds(after, limit):
    return get_cached(
        f'transit-land_{after}_{limit}',
        lambda: _get_transit_land_feeds(after, limit),
        directory='.cache/transit.land'
    )


def get_transit_land_urls(domains):
    content = get_transit_land_feeds(0, 10000)
    result = json.loads(content)
    onestop_ids = [e['onestop_id'] for e in result['data']['entities']]
    result_urls = []

    # TODO reading/parsing these files is slow. Move to transit_land.py and cache
    for onestop_id in onestop_ids:
        html = get_cached(
            onestop_id,
            lambda: get_transit_land_feed(onestop_id),
            directory='.cache/transit.land'
        )
        soup = BeautifulSoup(html, 'html.parser')
        for tag in soup.find_all('code'):
            url = tag.text
            domain, path = url_split(url)
            if domain in domains:
                result_urls.append(url)
    return result_urls
