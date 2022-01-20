from bs4 import BeautifulSoup
import urllib.parse
from urllib.error import HTTPError
import yaml

from cache import curl_cached
from utils import extract_urls

LOCATION = "67-california-usa"
ROOT = "https://transitfeeds.com"


def resolve_url(url):
    if url.startswith(ROOT):
        return url
    if url.startswith("/"):
        return f"{ROOT}{url}"
    raise ValueError("Not a transit feed url: {url}")


def get_transitfeeds_urls(domains):
    page_urls = []
    provider_urls = []
    feed_urls = []
    result_urls = set()

    html = curl_cached(f"{ROOT}/l/{LOCATION}")
    soup = BeautifulSoup(html, "html.parser")
    for a in soup.select(".pagination a"):
        page_urls.append(resolve_url(a["href"]))

    for page_url in page_urls:
        html = curl_cached(page_url)
        soup = BeautifulSoup(html, "html.parser")
        for a in soup.select("a.btn"):
            if a["href"].startswith("/p/"):
                provider_urls.append(resolve_url(a["href"]))

    for provider_url in provider_urls:
        html = curl_cached(provider_url)
        soup = BeautifulSoup(html, "html.parser")
        for a in soup.select("a.list-group-item"):
            feed_urls.append(resolve_url(a["href"]))

    for feed_url in feed_urls:
        try:
            html = curl_cached(feed_url)
        except HTTPError:
            print("failed to fetch:", feed_url)
            continue

        soup = BeautifulSoup(html, "html.parser")
        for a in soup.select("a"):
            url = a["href"]
            if url.startswith("/") or url.startswith(ROOT):
                continue
            domain = urllib.parse.urlparse(url).netloc
            if domain in domains:
                result_urls.add(url)
    return result_urls


if __name__ == "__main__":
    with open("agencies.yml", "r") as f:
        agencies_obj = yaml.load(f, Loader=yaml.SafeLoader)
    urls = extract_urls(agencies_obj, dict_prefix="gtfs_rt")
    domains = set()
    for url in urls:
        domains.add(urllib.parse.urlparse(url).netloc)
    for url in get_transitfeeds_urls(domains):
        if url in urls:
            print(url)
