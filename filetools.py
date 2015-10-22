#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

__author__ = """Co-Pierre Georg (co-pierre.georg@uct.ac.za)"""

import sys
import logging
import re

from math import ceil


#-------------------------------------------------------------------------
#
#  class Mapping
#
#-------------------------------------------------------------------------
class File(object):
    __version__ = 0.9


#
# VARIABLES
#
    identifier = ""


#
#  METHODS
#
    #-------------------------------------------------------------------------
    #  __init__
    #-------------------------------------------------------------------------
    def __init__(self):
        pass
    #-------------------------------------------------------------------------


    """
    This method reads in a large file with a predetermined number of lines and splits
    it into several smaller files.
    """
    def split_file(self, input_file_name, _num_lines, _num_files):
        num_lines = int(_num_lines)
        num_files = int(_num_files)

        input_file = open(input_file_name, "r")
        file_identifier = input_file_name.split('.')[0]  # used for input and output file name
        file_extension = input_file_name.split('.')[1]
        if len(input_file_name.split('.')) > 2:
            raise AssertionError("File name must contain only a single . as separator between identifier and extension.")
            exit

        lines_to_read = ceil(num_lines/num_files)

        #
        # read all lines in the input file, every so often, write them into a new output file
        #
        i = 0
        num_file = 0

        out_text = ""
        for line in input_file.readlines():
            if i < lines_to_read:
                out_text += line + "\n"
                i += 1
            else:
                out_file_name = file_identifier + "-" + str(num_file) + "." + file_extension
                print out_file_name
                out_file = open(out_file_name, 'w')
                out_file.write(out_text)
                out_file.close()

                out_text = ""  # reset out_text
                num_file += 1  # increase file count
                i = 0 # and reset line count