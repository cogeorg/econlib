#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

"""
Robustness check for Agent-Based Models (conceivably other models as well) across the whole of the multidimensional
parameter space.

Author: Co-Pierre Georg (cogeorg@gmail.com)

Version: 0.1

Date of last update: 12-09-2015 (Cape Town)

"""

# Libraries
import sys
import math

from conftools import Config

# ---------------------------------------------------------------------------
#
# CLASS ParallelTools
#
# ---------------------------------------------------------------------------
class ParallelTools(object):
    __version__ = 0.1

    """
    Parameters
    """
    #

    """
    Functions
    """

    def __init__(self):
        self.num_runs = 0
        self.num_cores = 0
        self.runs_per_core = 0
        self.runs_last_core = 0


    def create_parallel_config_file(self, control_config, template_config, counter):
        # the number of runs depends on the core we look at
        if counter < self.num_cores - 1:
            num_runs = self.runs_per_core
        else:
            num_runs = self.runs_last_core

        # numbering of output_files is done by number of cores
        out_str = "<config identifier='" + control_config.identifier + "-" + str(counter) + "'>\n"
        out_str += "  <parameter type='static' name='runs' value='" + str(num_runs) + "'></parameter>\n"

        # the other static parameters remain the same
        for entry in template_config.static_parameters:
            value = template_config.static_parameters[entry]
            out_str += "  <parameter type='static' name='" + entry + "' value='" + str(value) + "'></parameter\n"

        # find variable parameter keys
        param_keys = sorted(template_config.variable_parameters.keys())
        # then write out the variable parameters
        for other_key in param_keys:
            from_value = template_config.variable_parameters[other_key][0]
            to_value = template_config.variable_parameters[other_key][1]
            out_str += "  <parameter type='variable' name='" + other_key + "' range='" + str(from_value) + "-" + \
                       str(to_value) + "'></parameter>\n"
        out_str += "</config>"

        # we don't return anything if number of runs equals zero
        if num_runs != 0:
            return out_str

    def create_config_files(self, config_file_name):
        # first, read the config file to find out the number of cores, etc.
        control_config = Config()
        control_config.read_xml_config_file(config_file_name)

        template_config_file_name = control_config.static_parameters['template_config_file']
        template_config = Config()
        template_config.read_xml_config_file(template_config_file_name)

        # create config files computes the optimal split of a template config file with N parameter runs across K cores
        self.num_runs = int(control_config.static_parameters['num_runs'])

        # the number of config files we create equals the number of cores
        self.num_cores = int(control_config.static_parameters['num_cores'])

        # the number of simulations we run on each core is the total number of simulations divided by the number of
        # cores minus one. the remainder of the modulo will be run on the last core to make sure we end up with
        # exactly N simulations in total
        self.runs_per_core = int(math.floor(self.num_runs / (self.num_cores-1)))
        self.runs_last_core = self.num_runs % (self.num_cores-1)

        # now create config files for all cores
        for i in range(0, self.num_cores):
            out_str = self.create_parallel_config_file(control_config, template_config, i)
            # write the output file
            if out_str != None:
                output_file_name = control_config.static_parameters['output_basefile_name'] + "-" + str(i) + ".xml"
                output_file = open(output_file_name, "w")
                output_file.write(out_str)
                output_file.close()
