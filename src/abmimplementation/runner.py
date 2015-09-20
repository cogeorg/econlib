#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from random import Random

from src.abmimplementation.config import Config
from src.abmimplementation.model import Model

class Runner(object):
    identifier = ""

    def __init__(self, config):
        self.identifier = config.identifier
        self.num_simulations = int(config.static_parameters['num_simulations'])

        # the template contains the valid ranges for parameters
        self.model_config_template = Config()
        model_config_file_name = config.get_static_parameters()['model_config_file_name']
        self.model_config_template.read_xml_config_file(model_config_file_name)
        # this is the model_config that is used for a given simulation
        self.model_config = Config()


    def generate_model_config(self, model_config_template):
        self.model_config.identifier = self.model_config_template.identifier
        for entry in model_config_template.static_parameters:
            self.model_config.static_parameters[entry] = model_config_template.static_parameters[entry]
        # loop over all variable parameters and generate a random draw; create a static parameter in model_config
        for entry in model_config_template.variable_parameters:
            lower = model_config_template.variable_parameters[entry][0]
            upper = model_config_template.variable_parameters[entry][1]
            random = Random()
            value = random.uniform(lower, upper)
            self.model_config.static_parameters[entry] = value


    def do_run(self):
        for i in range(0, self.num_simulations):
            # generate model parameters from runner_config
            self.generate_model_config(self.model_config_template)
            self.model_config.identifier = self.model_config.identifier + "-" + str(i)

            model = Model(self.model_config)
            model.initialize_agents()

            model.do_update()

