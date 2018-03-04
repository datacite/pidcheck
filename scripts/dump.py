""" A helper script to dump results into a file """
import sys
import os
import json
import logging
import csv

import pidcheck

# Configure basic logging
logging.basicConfig(level=logging.INFO)

def dump_csv(filename, results):
    """Write to results to CSV"""
    with open(filename, 'w') as f:
        # Just use the first results keys as field names,
        # note this isn't a guaranteed order
        w = csv.DictWriter(f, results[0].keys())
        w.writeheader()

        for result in results:
            w.writerow(result)

if __name__ == '__main__':
    # Get the results
    results = pidcheck.pop_current_results()

    if not results:
        logging.warn("No results")
        sys.exit()

    # Dump
    filename = sys.argv[1]
    if filename.endswith('.csv'):
        dump_csv(filename, results)
    else:
        raise Exception("No known handling for extension")

    logging.info("Wrote to " + filename)