# Feed Checker

This repo is to verify that a given list of feeds is listed in feed aggregators.
Currently it checks transit.land and transitfeeds.com to verify that feeds are
listed in an aggregator.

## Installation

```
pip install calitp-feed-checker
```

## Configure

The following env variables can be set in a `.env` file, set to the environment,
or inline like `TRANSITLAND_API_KEY=SECRET python -m feed_checker [...]`.

* `TRANSITLAND_API_KEY` An [api key from transitland][1].

* `CALITP_CACHE_DIR` Folder to save cached files to. Defaults to
`~/.cache/calitp_feed_checker`

## Getting Started

## CLI Usage

`python -m feed_checker [YAML_FILE] [OPTIONS]`

`python -m feed_checker` or `python -m feed_checker /path/to/yml` will search a
[Cal-ITP agencies.yml file][2] for any urls and see if they are present in any
of the feed aggregators. Alternatively you can use a `--csv-file` or `--url`
instead of an `agencies.yml` file.

The final line of stdout will tell how many urls were in `agencies.yml` and how
many of those were matched in a feed.

### Options
* `python -m feed_checker --help` print the help
* `--csv-file agencies.csv` load a csv instead of a Cal-ITP agencies yaml file
  (one url per line)
* `--url http://example.com` Check a single url instead of a Cal-ITP agencies
  yaml file
* `--verbose` Print a table of all results (organized by domain)
* `--output /path/to/file.json` Save the results as a json file
* `--clear-cache` Deletes the cache folder before running.

[1]: https://www.transit.land/documentation/index#signing-up-for-an-api-key
[2]: https://github.com/cal-itp/data-infra/blob/main/airflow/data/agencies.yml

## Development

Clone this repo and `pip install -e /pat/to/feed-checker` to develop locally.

By default, downloaded files (raw html files, api requsets) will be saved to
`~/.cache/calitp_feed_checker`. This greatly reduces the time required to run
the script. Delete this folder to reset the cache.
