from dotenv import load_dotenv
import json
import os
import urllib.parse
import urllib.request

from cache import curl_cached, JsonCache
from utils import url_split

load_dotenv()
BASE_URL = "https://api.transit.land/api/v1/"
API_KEY = os.environ["TRANSITLAND_API_KEY"]


def get_transitland_feed(feed_id):
    feed_id = urllib.parse.quote(feed_id)
    url = f"{BASE_URL}feeds/{feed_id}?apikey={API_KEY}"
    return json.loads(curl_cached(url, key=feed_id))


def get_feed_ids():
    url = f"{BASE_URL}operators?apikey={API_KEY}"
    url += "&per_page=10000&total=true"
    operators = json.loads(curl_cached(url, key="transitland_operators"))
    results = []
    for operator in operators["operators"]:
        results += operator["represented_in_feed_onestop_ids"]
    return sorted(list(set(results)))


def get_transitland_urls(domains):
    feed_ids = get_feed_ids()[::-1]
    result_urls = []
    skip_ids = JsonCache("transit_land_skip_ids")

    # TODO reading/parsing these files is slow.
    for feed_id in feed_ids:
        if feed_id in skip_ids:
            print("skipping", feed_id)
            continue
        try:
            feed = get_transitland_feed(feed_id)
        except urllib.error.HTTPError as e:
            print("Failed to get feed for feed_id: ", feed_id, e.getcode())
            if e.getcode() == 500:
                print("^---- adding to skip_ids because 500")
                skip_ids[feed_id] = True
            continue
        for urls in feed["urls"].values():
            if isinstance(urls, str):
                # values can be a string or list of strings, normalize them
                urls = [urls]
            for url in urls:
                domain, _ = url_split(url)
                if domain in domains:
                    result_urls.append(url)
    return result_urls


if __name__ == "__main__":
    get_transitland_urls([])
