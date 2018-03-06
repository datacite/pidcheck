"""A helper module for working with the PidCheck crawler results"""

import sys
import os
import json
import redis
import logging

# Basic settings
START_URLS_KEY = os.getenv('START_URLS_KEY', 'pidcheck:start_urls')
RESULTS_ITEMS_KEY = os.getenv('REDIS_ITEMS_KEY', 'pidcheck:items')

REDIS_HOST = os.getenv('REDIS_HOST', 'localhost')
REDIS_PORT = os.getenv('REDIS_PORT', 6379)

# Redis server connector
redis = redis.StrictRedis(host=REDIS_HOST, port=REDIS_PORT, db=0)

def push_pid(pid, url):
    """Push a url into redis for processing by the crawler"""
    pl = {'pid': pid, 'url': url}
    logging.info("Queueing '{0}' with url '{1}' for processing".format(pid, url))
    redis.lpush(START_URLS_KEY, json.dumps(pl))

def pop_result():
    """Pop one pidcheck result from redis"""
    raw = redis.rpop(RESULTS_ITEMS_KEY)
    if raw:
        result = json.loads(raw)
        logging.info("Popped result for '{0}' with url '{1}'".format(result['pid'], result['checked_url']))
        return result
    else:
        return None

def pop_current_results():
    """Retrieve current batch of results from the redis server"""
    results = []
    for i in range( redis.llen(RESULTS_ITEMS_KEY) ):
        results.append(pop_result())

    return results
