""" A helper script to seed PID's into the crawler """
import sys
import os
import json
import logging
import csv

import pidcheck

# Configure basic logging
logging.basicConfig(level=logging.INFO)

def seed_jsonl(filename):
    """Seed from jsonl file format"""
    with open(filename) as f:
        for jl in f:
            url = json.loads(jl)
            pidcheck.push_pid(url['pid'], url['url'])

def seed_csv(filename):
    """Seed from csv file"""
    with open(filename) as f:
        r = csv.DictReader(f, ['pid', 'url'])
        for row in r:
            pidcheck.push_pid(row['pid'], row['url'])

if __name__ == '__main__':
    logging.info("Starting seeding")

    filename = sys.argv[1]
    if filename.endswith('.csv'):
        seed_csv(filename)
    elif filename.endswith('.jsonl'):
        seed_jsonl(filename)
    else:
        raise Exception("No known handling for extension")