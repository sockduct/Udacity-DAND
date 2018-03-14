#!/usr/bin/env python3

# Generate random sample from CSV

import csv
import os
import random
import sys

# Use system RNG, better entropy:
RNG = random.SystemRandom()
# How many rows to get for sample:
SAMPLE = 10000


def main(argv):
    if len(argv) != 2:
        callname = os.path.basename(argv[0])
        sys.exit('Usage:  {} <csv-file>'.format(callname))

    csvfile = argv[1]
    if not os.path.isfile(csvfile):
        sys.exit('Error:  Invalid file - {}'.format(csvfile))

    # For entire file to sample rows:
    dataset = []
    # For resulting sample file:
    sampleset = []
    with open(csvfile) as infile:
        # Get header row:
        sampleset.append(infile.readline())

        # Collect rest of file rows
        for row in infile:
            dataset.append(row)

    # Get a sample
    sampleset.extend(RNG.sample(dataset, SAMPLE))
    csvout = os.path.splitext(csvfile)[0] + '-sample' + os.path.splitext(csvfile)[1]
    with open(csvout, 'w') as outfile:
        for line in sampleset:
            outfile.write(line)

    print('{} created with header row and {:,} sample rows from {}.'.format(
          csvout, SAMPLE, csvfile))


if __name__ == '__main__':
    main(sys.argv)

