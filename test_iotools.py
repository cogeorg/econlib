#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = """Michael Rose (Michael.Q.Rose@gmail.com)"""

#-------------------------------------------------------------------------
#
#  iotools.py is a simple module to input and output csv files
#
#-------------------------------------------------------------------------
if __name__ == '__main__':

#
# VARIABLES
#
    import sys
    import pprint

    import iotools

    # we have multiple tests here, the first argument specifies which test
    # to run
    test_number = sys.argv[1]

    #
    # TEST 1: read csv to dictionary
    #
    if test_number == "1":
        input_file = sys.argv[2]

        print "IOTools version: " + str(iotools.io.__version__)
        print "Read " + input_file + " as:"

        german_peace_nobel_laureates = iotools.csv_to_dict(input_file, lambda row: " ".join(row[:2]), lambda row: row[2])

        pprint.pprint(german_peace_nobel_laureates)

