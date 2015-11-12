#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = """Michael E. Rose (Michael.Ernst.Rose@gmail.com)"""

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

    import src.iotools as iotools

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

    #
    # TEST 1: read csv to nested dictionary
    #
    if test_number == "2":
        input_file = sys.argv[2]

        print "IOTools version: " + str(iotools.io.__version__)
        print "Read " + input_file + " as:"

        german_peace_nobel_laureates_nested = iotools.csv_to_nested_dict(input_file, lambda row: row.pop('year'))

        pprint.pprint(german_peace_nobel_laureates_nested)

    #
    # TEST 2: output nested dictionary to csv
    #
    if test_number == "3":
        output_name = sys.argv[2]

        print "IOTools version: " + str(iotools.io.__version__)
        print "Print the following as: " + output_name

        largest_countries_eu = {}
        largest_countries_eu['Germany'] = {}
        largest_countries_eu['Germany']['Capital'] = "Berlin"
        largest_countries_eu['Germany']['Population'] = 81890000
        largest_countries_eu['France'] = {}
        largest_countries_eu['France']['Capital'] = "Paris"
        largest_countries_eu['France']['Population'] = 65697000
        largest_countries_eu['France']['Language'] = "French"
        largest_countries_eu['UK'] = {}
        largest_countries_eu['UK']['Capital'] = "London"
        largest_countries_eu['UK']['Population'] = 63228000
        largest_countries_eu['UK']['Seen'] = "yes"
        largest_countries_eu['Italy'] = {}
        largest_countries_eu['Italy']['Capital'] = "Rome"
        largest_countries_eu['Italy']['Population'] = 60918000

        pprint.pprint(largest_countries_eu)

        iotools.nested_dict_to_csv(largest_countries_eu, output_name, "country")
