#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from abmtemplate.baseconfig import BaseConfig

class Config(BaseConfig):
    """
    Class variables: identifier, static_parameters, variable_parameters
    """
    identifier = ""
    static_parameters = {}
    variable_parameters = {}

    def __init__(self):
        super(Config, self).__init__()

    def get_identifier(self):
        return self.identifier

    def set_identifier(self, _value):
        """
        Class variables: identifier
        Local variables: _identifier
        """
        super(Config, self).set_identifier(_value)

    def get_static_parameters(self):
        return self.static_parameters

    def set_static_parameters(self, _value):
        """
        Class variables: static_parameters
        Local variables: _params
        """
        super(Config, self).set_static_parameters(_value)

    def get_variable_parameters(self):
        return self.variable_parameters

    def set_variable_parameters(self, _value):
        """
        Class variables: variable_parameters
        Local variables: _params
        """
        super(Config, self).set_variable_parameters(_value)

    def __str__(self):
        """
        Class variables: identifier, static_parameters, variable_parameters
        Local variables: out_str, entry, value, from_value, to_value
        """
        return super(Config, self).__str__()

    def read_xml_config_file(self, _config_file_name):
        """
        Class variables: identifier, static_parameters, variable_parameters
        Local variables: xmlText, config_file_name, element, subelement, name, value, format_correct, range_from, range_to
        """
        super(Config, self).read_xml_config_file(_config_file_name)