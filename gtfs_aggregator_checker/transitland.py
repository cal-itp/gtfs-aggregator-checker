import json

from .config import env
from .cache import curl_cached

API_KEY = env["TRANSITLAND_API_KEY"]
BASE_URL = f"https://transit.land/api/v2/rest/feeds?apikey={API_KEY}"
BASE_URL += "&limit=1000"


def get_feeds(after=None):
    url = BASE_URL
    if after:
        url += f"&after={after}"
    text = curl_cached(url, key=f"feeds_after__{after}")
    data = json.loads(text)
    results = []
    for feed in data["feeds"]:
        for urls in feed["urls"].values():
            if isinstance(urls, str):
                urls = [urls]
            for url in urls:
                results.append(
                    (f"https://transit.land/feeds/{feed['onestop_id']}", url)
                )
    after = None
    if "meta" in data:
        after = data["meta"]["after"]
    return list(results), after


def get_transitland_urls():
    urls, after = get_feeds()
    while True:
        new_urls, after = get_feeds(after)
        urls += new_urls
        if not after:
            break
    return urls
