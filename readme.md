PidCheck
--------

PidCheck is a generic crawler for extracting data about PiD's from landing pages and doing some calculation on the health of the link.
It is based upon the [Scrapy](https://scrapy.org/) framework for doing most of the hard work.
It is configured for broad crawling to hit multiple domains and does this in a polite way by default.

## Requirements

Python 3
Scrapy

## Install

`pip install -r requirements.txt`

## CLI Run:

`scrapy crawl pid -a url_file=urls.jl -o test.jl`

url_file - An input filename for a json lines file that looks like:

```
{ "pid": "msk0-7250", "url": "https://doi.org/10.5438/msk0-7250" }
{ "pid": "msk0-7250", "url": "https://blog.datacite.org/datacite-hiring-another-application-developer/" }
{ "pid": "ea4h-tx3g", "url": "https://doi.org/10.5438/ea4h-tx3g" }
```