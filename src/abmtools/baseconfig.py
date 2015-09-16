#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = """Co-Pierre Georg (co-pierre.georg@uct.ac.za)"""

import abc

# -------------------------------------------------------------------------
#
#  class Config
#
# -------------------------------------------------------------------------
class BaseConfig(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def get_identifier(self):
        return
    @abc.abstractmethod
    def set_identifier(self, _identifier):
        if not isinstance(_identifier, str):
            raise TypeError
        else:
            self.identifier = _identifier
        return
    identifier = abc.abstractproperty(get_identifier, set_identifier)

    @abc.abstractmethod
    def get_static_parameters(self):
        return
    @abc.abstractmethod
    def set_static_parameters(self, _params):
        if not isinstance(_params, dict):
            raise TypeError
        else:
            self.identifier = _params
        return
    static_parameters = abc.abstractproperty(get_static_parameters, set_static_parameters)

    @abc.abstractmethod
    def get_variable_parameters(self):
        return
    @abc.abstractmethod
    def set_variable_parameters(self, _params):
        if not isinstance(_params, dict):
            raise TypeError
        else:
            self.identifier = _params
        return
    variable_parameters = abc.abstractproperty(get_variable_parameters, set_variable_parameters)