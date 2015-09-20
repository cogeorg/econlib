#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from abmtemplate.baseconfig import BaseConfig

class Config(BaseConfig):
    identifier = ""
    static_parameters = {}
    variable_parameters = {}

    def __init__(self):
        super(Config, self).__init__()

    def get_identifier(self):
        return self.identifier

    def set_identifier(self, _value):
        super(Config, self).set_identifier(_value)

    def get_static_parameters(self):
        return self.static_parameters

    def set_static_parameters(self, _value):
        super(Config, self).set_static_parameters(_value)

    def get_variable_parameters(self):
        return self.variable_parameters

    def set_variable_parameters(self, _value):
        super(Config, self).set_variable_parameters(_value)

    def __str__(self):
        return super(Config, self).__str__()

    def read_xml_config_file(self, _config_file_name):
        super(Config, self).read_xml_config_file(_config_file_name)