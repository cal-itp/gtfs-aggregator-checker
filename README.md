# Feed Checker

This repo is to verify that a given list of feeds is listed in feed aggregators.
Currently it checks transit.land and transitfeeds.com to verify that feeds are
listed in an aggregator.


## Usage

First place an `agencies.yml` file in this folder. This file can have any
structure but only urls on lines matching the regexp `gtfs_rt.*: https?://.*`
will be considered. To check urls run the following. The first time you run this
it will take a while since the cache is dry.

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
