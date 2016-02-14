__author__ = """Co-Pierre Georg (co-pierre.georg@uct.ac.za)"""

import sys
import logging
import re


#-------------------------------------------------------------------------
#
#  class Node
#
#-------------------------------------------------------------------------
class Node(object):
    __version__ = 0.9

#
# VARIABLES
#
    identifier = ""
    in_degree = 0
    out_degree = 0

#
# METHODS
#
    #-------------------------------------------------------------------------
    #  __init__
    #-------------------------------------------------------------------------
    def __init__(self, _identifier):
        self.identifier = _identifier
    #-------------------------------------------------------------------------
