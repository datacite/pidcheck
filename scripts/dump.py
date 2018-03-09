""" A helper script to dump results into a file """
import sys
import os
import json
import logging
import csv

import pidcheck

# Configure basic logging
logging.basicConfig(level=logging.INFO)

def dump_csv(filename):
    """Write to results to CSV"""
    with open(filename, 'w') as f:

        fields = [
            'pid',
            'checked_url',
            'http_status',
            'error',
            'checked_date',
            'schema_org_id',
            'dc_identifier',
            'citation_doi',
            'pid_meta_match',
            'pid_meta_different',
            'body_has_pid'
        ]

        result = pidcheck.pop_result()
        if result:
            w = csv.DictWriter(f, fields, extrasaction='ignore')
            w.writeheader()

            while result:
                w.writerow(result)
                result = pidcheck.pop_result()

            logging.info("Wrote data to " + filename)
        else:
            logging.info("No items found, nothing to dump")


if __name__ == '__main__':

    # Dump
    filename = sys.argv[1]
    if filename.endswith('.csv'):
        dump_csv(filename)
    else:
        raise Exception("No known handling for extension")