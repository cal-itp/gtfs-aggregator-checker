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

* help: `python feed_checker.py --help`
* YAML file: `python feed_checker.py` or `python feed_checker.py /path/to/yml`
* CSV file: `python feed_checker.py --csv-file agencies.csv` (one url per line)
* Single URL: `python feed_checker.py --url http://example.com`
