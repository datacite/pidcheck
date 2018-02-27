""" A helper script to seed PID's into the crawler """
import sys
import os
import json
import logging

import pidcheck

# Configure basic logging
logging.basicConfig(level=logging.INFO)

def parse_jsonl(filename):
    """Parse jsonl file format"""
    with open(filename) as f:
        for jl in f:
            url = json.loads(jl)
            pidcheck.push_pid(url['pid'], url['url'])

def load_from_file(filename):
    """Load seed urls from a filename"""
    if filename.endswith('.jsonl'):
        parse_jsonl(filename)

if __name__ == '__main__':
    logging.info("Starting seeding")
    load_from_file(sys.argv[1])