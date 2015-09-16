#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = """Co-Pierre Georg (co-pierre.georg@uct.ac.za)"""

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

    #
    #  METHODS
    #
    # -------------------------------------------------------------------------
    #  __init__
    # -------------------------------------------------------------------------
    def __init__(self):
        self.identifier = ""
        self.static_parameters = {}
        self.variable_parameters = {}


    # -------------------------------------------------------------------------
    #  __str__
    # -------------------------------------------------------------------------
    def __str__(self):
        out_str = "<config identifier='" + self.identifier + "'>\n"
        for entry in self.static_parameters:
            value = self.static_parameters[entry]
            out_str += "  <parameter type='static' name='" + entry + "' value='" + str(value) + "'></parameter\n"
        for entry in self.variable_parameters:
            from_value = self.variable_parameters[entry][0]
            to_value = self.variable_parameters[entry][1]
            stepwidth = self.variable_parameters[entry][2]
            out_str += "  <parameter type='variable' name='" + entry + "' range='" + str(from_value) + "-" + \
                       str(to_value) + "' stepwidth='" + str(stepwidth) + "'></parameter>\n"
        out_str += "</config>"

        return out_str


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

            if subelement.attrib['type'] == 'static':
                try:  # we see whether the value is a float
                    value = float(subelement.attrib['value'])
                except:  # if not, it is a string
                    value = str(subelement.attrib['value'])
                self.static_parameters[name] = value

            if subelement.attrib['type'] == 'variable':
                format_correct = True

                try:
                    range_from = float(subelement.attrib['range'].rsplit("-")[0])
                except:
                    format_correct = False
                    print "<< CONFTOOLS: range_from must be a float or int. Found: " + str(subelement.attrib['range'].rsplit("-")[0])

                try:
                    range_to = float(subelement.attrib['range'].rsplit("-")[1])
                except:
                    format_correct = False
                    print "<< CONFTOOLS: range_to must be a float or int. Found: " + str(subelement.attrib['range'].rsplit("-")[1])

                if format_correct:
                    self.variable_parameters[name] = [range_from, range_to]
                else:
                    print "<< CONFTOOLS: FOUND ERROR IN FILE " + config_file_name + ", ABORTING"
    #-------------------------------------------------------------------------
