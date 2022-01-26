import typer
import urllib.error
import urllib.parse
import urllib.request
import yaml

from cache import url_split
from transitland import get_transitland_urls
from transitfeeds import get_transitfeeds_urls
from utils import extract_urls


def clean_url(url):
    url = urllib.parse.urlparse(url)
    query = urllib.parse.parse_qs(url.query, keep_blank_values=True)
    query.pop("api_key", None)
    query.pop("token", None)
    url = url._replace(query=urllib.parse.urlencode(query, True))
    return urllib.parse.urlunparse(url)


def tabulate(columns):
    column_sizes = [max([len(s) for s in column]) for column in columns]
    num_rows = max([len(column) for column in columns])
    for i_row in range(num_rows):
        row = []
        for i_col, column in enumerate(columns):
            value = column[i_row] if len(column) > i_row else ""
            size = column_sizes[i_col]
            row.append(f"{value:<{size}}")
        print("   ".join(row))


def main(
    yml_file=typer.Argument("agencies.yml"), prefix=typer.Option("gtfs_"),
):
    domains = {}

    with open(yml_file, "r") as f:
        agencies_obj = yaml.load(f, Loader=yaml.SafeLoader)
    urls = extract_urls(agencies_obj)
    for url in urls:
        url = clean_url(url)
        domain, path = url_split(url)
        if domain not in domains:
            domains[domain] = {
                "in_yml": [],
                "in_feeds": [],
            }
        domains[domain]["in_yml"].append(path)

    for url in get_transitland_urls(domains):
        domain, path = url_split(clean_url(url))
        domains[domain]["in_feeds"].append(path)

    for url in get_transitfeeds_urls(domains):
        domain, path = url_split(clean_url(url))
        domains[domain]["in_feeds"].append(path)

    counts = {"matched": 0, "total": 0}
    for domain in sorted(domains.keys()):
        matched = ["matched"]
        missing = ["missing"]
        unused = ["unused"]
        for path in domains[domain]["in_yml"]:
            counts["total"] += 1
            if path in domains[domain]["in_feeds"]:
                counts["matched"] += 1
                matched.append(path)
            else:
                missing.append(path)
        for path in domains[domain]["in_feeds"]:
            if path not in domains[domain]["in_yml"]:
                unused.append(path)
        print(f"\n{domain}")
        tabulate([matched, missing, unused])
    print(f'Matched {counts["matched"]} / {counts["total"]} urls')


if __name__ == "__main__":
    typer.run(main)
