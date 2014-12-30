#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = """Co-Pierre Georg (co-pierre.georg@uct.ac.za)"""

import sys
import logging

#-------------------------------------------------------------------------
#
#  class Config
#
#-------------------------------------------------------------------------
class Config(object):
    __version__ = 0.9

    #
    # VARIABLES
    #
    identifier = ""
    static_parameters = {}
    changing_parameters = {}

    #
    #  METHODS
    #
    #-------------------------------------------------------------------------
    #  __init__
    #-------------------------------------------------------------------------
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
            value = float(subelement.attrib['value'])
            if (subelement.attrib['type'] == 'static'):
                self.static_parameters[name] = value
            if (subelement.attrib['type'] == 'changing'):
                valid_from = subelement.attrib['validity'].rsplit("-")[0]
                valid_to = subelement.attrib['validity'].rsplit("-")[1]
                self.changing_parameters[name] = [value, valid_from, valid_to]
    #-------------------------------------------------------------------------
