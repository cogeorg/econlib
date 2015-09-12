#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = """Co-Pierre Georg (co-pierre.georg@uct.ac.za)"""

import sys
import logging

# -------------------------------------------------------------------------
#
#  class Config
#
# -------------------------------------------------------------------------
class Config(object):
    __version__ = 0.9

    #
    # VARIABLES
    #
    identifier = ""
    static_parameters = {}
    variable_parameters = {}

    #
    #  METHODS
    #
    # -------------------------------------------------------------------------
    #  __init__
    # -------------------------------------------------------------------------
    def __init__(self):
        pass


    #-------------------------------------------------------------------------
    # read_xml_config_file
    #-------------------------------------------------------------------------
    def read_xml_config_file(self, config_file_name):
        from xml.etree import ElementTree
        xmlText = open(config_file_name).read()
        element = ElementTree.XML(xmlText)
        self.identifier = element.attrib['identifier']

        # loop over all entries in the xml file
        for subelement in element:
            name = subelement.attrib['name']
            if (subelement.attrib['type'] == 'static'):
                try:  # we see whether the value is a float
                    value = float(subelement.attrib['value'])
                except:  # if not, it is a string
                    value = str(subelement.attrib['value'])
                self.static_parameters[name] = value
            if (subelement.attrib['type'] == 'variable'):
                format_correct = True
                try:
                    value = float(subelement.attrib['range'].rsplit("-")[0])
                    range_from = value
                except:
                    format_correct = False
                    print "<< CONFTOOLS: range_from must be a float or int. Found: " + str(subelement.attrib['range'].rsplit("-")[0])
                try:
                    value = float(subelement.attrib['range'].rsplit("-")[1])
                    range_to = value
                except:
                    format_correct = False
                    print "<< CONFTOOLS: range_to must be a float or int. Found: " + str(subelement.attrib['range'].rsplit("-")[1])
                try:
                    value = subelement.attrib['stepwidth']
                    stepwidth = float(value)
                except:
                    format_correct = False
                    print "<< CONFTOOLS: stepwidth must be a float or int. Found: " + str(subelement.attrib['stepwidth'])
                if format_correct:
                    self.variable_parameters[name] = [range_from, range_to, stepwidth]
                else:
                    print "<< CONFTOOLS: FOUND ERROR IN FILE " + config_file_name + ", ABORTING"
    #-------------------------------------------------------------------------
