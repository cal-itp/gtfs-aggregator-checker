# Feed Checker

This repo is to verify that a given list of feeds is listed in feed aggregators.
Currently it checks transit.land and transitfeeds.com to verify that feeds are
listed in an aggregator.


## Requirements

* `.env` - Acquire an [api key from transitland][1] and save it to a `.env` file
  like `TRANSITLAND_API_KEY=SECRET`. Alternatively you can prefix commands with
  the api key like `TRANSITLAND_API_KEY=SECRET python feed_checker.py [...]`.

* `agencies.yml` - This file can have any structure as the feed checker just
  looks for any urls (strings starting with `'http://'`), but the intended usage
  is a [Cal-ITP agencies.yml file][2]. (to run the program without an
  `agencies.yml` file, see the "Options" section below)

## Getting Started

To install requirments and check urls run the following. The first time you run
this it will take a while since the cache is empty.

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
[Cal-ITP agencies.yml file][2] for any urls and see if they are present in any
of the feed aggregators.

### Options
* `python feed_checker.py --help` print the help
* `--csv-file agencies.csv` load a csv instead of a Cal-ITP agencies yaml file (one url per line)
* `--url http://example.com` Check a single url instead of a Cal-ITP agencies yaml file
* `--verbose` Print a table of all results (organized by domain)
* `--output /path/to/file.json` Save the results as a json file

[1]: https://www.transit.land/documentation/index#signing-up-for-an-api-key
[2]: https://github.com/cal-itp/data-infra/blob/main/airflow/data/agencies.yml
