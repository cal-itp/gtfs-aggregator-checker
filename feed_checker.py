import json
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


def tabulate(data, column_names):
    columns = []
    for name in column_names:
        columns.append([name, *data[name]])
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
    yml_file=typer.Argument("agencies.yml", help="A yml file containing urls"),
    csv_file=typer.Option(None, help="A csv file (one url per line)"),
    url=typer.Option(None, help="URL to check instead of a file",),
    output=typer.Option(None, help="Path to a file to save output to."),
    verbose: bool = typer.Option(False, help="Print a result table to stdout"),
):
    domains = {}

    if url:
        urls = [url]
    elif csv_file:
        with open(csv_file, "r") as f:
            urls = f.read().strip().splitlines()
    else:
        with open(yml_file, "r") as f:
            agencies_obj = yaml.load(f, Loader=yaml.SafeLoader)
        urls = extract_urls(agencies_obj)
    urls = list(set([url.strip() for url in urls]))
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
    results = {}
    for domain in sorted(domains.keys()):
        results[domain] = {
            "matched": [],
            "missing": [],
            "unused": [],
        }
        for path in domains[domain]["in_yml"]:
            counts["total"] += 1
            if path in domains[domain]["in_feeds"]:
                counts["matched"] += 1
                results[domain]["matched"].append(path)
            else:
                results[domain]["missing"].append(path)
        for path in domains[domain]["in_feeds"]:
            if path not in domains[domain]["in_yml"]:
                results[domain]["unused"].append(path)
        if verbose:
            print(f"\n{domain}")
            tabulate(results[domain], ["matched", "missing", "unused"])
    if output:
        with open(output, "w") as f:
            f.write(json.dumps(results, indent=4))
            print(f"Results saved to {output}")
    print(f'Matched {counts["matched"]} / {counts["total"]} urls')


if __name__ == "__main__":
    typer.run(main)
