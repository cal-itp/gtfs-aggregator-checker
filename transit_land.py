from cache import get_cached
import json
import urllib.parse
import urllib.request


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
        directory='.cache/transit_land'
    )
