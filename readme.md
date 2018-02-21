PidCheck
--------

PidCheck is a generic crawler for extracting data about PiD's from landing pages and doing some calculation on the health of the link.
It is based upon the [Scrapy](https://scrapy.org/) framework for doing most of the hard work.
It is configured for broad crawling to hit multiple domains and does this in a polite way by default.

While the project actually includes a basic non redis backed version, the architecture
is designed to have a redis store for both feeding urls to check and storing the data for further
processing.

# Getting started with docker

For starting a version of the crawler and a redis, you can just do regular
`docker-compose up`

For debugging purposes you can use the seperate debug compose file
`docker-compose -f docker-compose.debug.yml up`

With this running you can push data into redis using redis-cli:

`src/redis-cli -p 32769 lpush pidcheck:start_urls '{ "pid": "msk0-7250", "url": "https://blog.datacite.org/datacite-hiring-another-application-developer/" }'`

## Settings

The following are important settings that you can override with environment variables.
It is possible to use a .env file for changing these settings as well.

USER_AGENT - Specify a user agent so sites can identify your bot. default: pidcheck
LOG_LEVEL - Standard python logging levels can be set, default: INFO
REDIS_HOST - Host for specifying a different redis* default: redis
REDIS_PORT - Port for specifiying a different redis* default: 6379

* Note specifying a different redis, you will want to use only the crawler docker image and
not the redis one.

# Development

## Requirements

* Python 3

## Install python libraries

`pip install -r requirements.txt`

## CLI Run:

From the crawler directory you can use the non redis version:

`scrapy crawl pidcheck-jl -a url_file=urls.jl -o test.jl`

url_file - An input filename for a json lines file that looks like:

```
{ "pid": "msk0-7250", "url": "https://doi.org/10.5438/msk0-7250" }
{ "pid": "msk0-7250", "url": "https://blog.datacite.org/datacite-hiring-another-application-developer/" }
{ "pid": "ea4h-tx3g", "url": "https://doi.org/10.5438/ea4h-tx3g" }
```