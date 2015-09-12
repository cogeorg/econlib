#!/usr/bin/env python
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
    config = Config()
    config.read_xml_config_file(config_file_name)

    print config.static_parameters
    print config.changing_parameters
