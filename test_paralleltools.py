#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

__author__ = """Co-Pierre Georg (co-pierre.georg@uct.ac.za)"""

import sys
from src.paralleltools import Parallel

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
    parallel = Parallel()
    parallel.create_config_files(config_file_name)
