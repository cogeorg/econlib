#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

__author__ = """Co-Pierre Georg (co-pierre.georg@uct.ac.za)"""

#-------------------------------------------------------------------------
#
#  conftools.py is a simple module to manage .xml configuration files
#
#-------------------------------------------------------------------------
if __name__ == '__main__':

#
# VARIABLES
#
    import sys

    from filetools import File

    args = sys.argv

    # we have multiple tests here, the first argument specifies which test
    # to run
    test_number = args[1]

    #
    # TEST 1: split_file
    #
    if test_number == "1":
        input_file_name = args[2]
        num_lines = args[3]
        num_files = args[4]

        file = File()

        file.split_file(input_file_name, num_lines, num_files)

