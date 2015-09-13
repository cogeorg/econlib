#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

__author__ = """Co-Pierre Georg (co-pierre.georg@uct.ac.za)"""

import sys
from paralleltools import ParallelTools

#-------------------------------------------------------------------------
#
#  conftools.py is a simple module to manage .xml configuration files
#
#-------------------------------------------------------------------------
if __name__ == '__main__':

    """
    VARIABLES
    """
    args = sys.argv
    config_file_name = args[1]

    """
    CODE
    """
    parallel = ParallelTools()
    parallel.create_config_files(config_file_name)
