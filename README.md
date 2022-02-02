# Feed Checker

This repo is to verify that a given list of feeds is listed in feed aggregators.
Currently it checks transit.land and transitfeeds.com to verify that feeds are
listed in an aggregator.


## Getting Started

First place an `agencies.yml` file in this folder. This file can have any
structure as the feed checker just looks for any urls (strings starting with
`'http://'`). To check urls run the following. The first time you run this it
will take a while since the cache is empty.

``` bash
pip install -r requirements.txt
python feed_checker.py
```

The final line of stdout will tell how many urls were in `agencies.yml` and how
many of those were matched in a feed. Above that it will list the domains for
each url (in alphabetical order) as well group paths based on if the path was
matched (in both `agencies.yml` and aggregator), missing (in `agencies.yml` but
not aggregator) or unused (in aggregator but not in `agencies.yml`). An ideal
outcome would mean the missing column is empty for all domains.

## CLI Usage

`python feed_checker.py` or `python feed_checker.py /path/to/yml` will search a
Cal-ITP [agencies.yml](https://github.com/cal-itp/data-infra/blob/main/airflow/data/agencies.yml) file for any urls and see if they are present in any of the feed
aggregators.

### Options
* `python feed_checker.py --help` print the help
* `--csv-file agencies.csv` load a csv instead of a yaml file (one url per line)
* `--url http://example.com` Check a single url instead of a yaml file
* `--verbose` Print a table of all results (organized by domain)
* `--output /path/to/file.json` Save the results as a json file
