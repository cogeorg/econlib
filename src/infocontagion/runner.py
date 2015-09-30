#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

from random import Random
from pprint import pprint

from src.infocontagion.config import Config
from src.infocontagion.model import Model

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
        # the result of each run is an optimum for a given (randomly drawn) parameter set
        self.results = []
        self.output_file_name = config.static_parameters['output_file_name']


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

    """
    get_out_text_header(model) is just a helper routine that prints the model parameters
    """
    def get_out_text_header(self, model):
        # start with runner parameters
        out_text = str(self.num_simulations) + ";"
        # add model parameters
        out_text += str(model.get_model_parameters()['num_agents']) + ";"
        out_text += str(model.get_model_parameters()['num_sweeps']) + ";"
        out_text += str(model.get_model_parameters()['R']) + ";"
        out_text += str(model.get_model_parameters()['beta']) + ";"
        out_text += str(model.get_model_parameters()['lambda']) + ";"
        out_text += str(model.get_model_parameters()['eta']) + ";"
        out_text += str(model.get_model_parameters()['phi']) + ";"
        out_text += str(model.get_model_parameters()['q']) + ";"
        out_text += str(model.get_model_parameters()['rho']) + ";"
        return out_text


    def write_results(self, model):
        out_text = ""
        # loop over all results
        for result in self.results:  # each result is a list (of lists) itself
            out_text += self.get_out_text_header(model)
            for entry in result:
                if isinstance(result, list):
                    for item in entry:
                        out_text += str(item) + ";"
                elif isinstance(result, str) or isinstance(result, int) or isinstance(result, float):
                    out_text += str(result) + ";"
                else:
                    print "    << ERROR in write_results", results_array
            out_text += "\n"

        out_file_name = self.output_file_name
        out_file = open(out_file_name, 'w')
        out_file.write(out_text)
        out_file.close()


    def do_run(self):
        for i in range(0, self.num_simulations):
            # generate model parameters from runner_config
            self.generate_model_config(self.model_config_template)
            self.model_config.identifier = self.model_config.identifier + "-" + str(i)

            model = Model(self.model_config)
            model.initialize_agents()
            result = model.do_update()

            self.results.append(result)
            self.write_results(model)

    def do_run_test_verbose(self):
        for i in range(0, self.num_simulations):
            # generate model parameters from runner_config
            self.generate_model_config(self.model_config_template)
            self.model_config.identifier = self.model_config.identifier + "-" + str(i)

            model = Model(self.model_config)
            model.initialize_agents()
            print("Initialized simulation #" +  str(i+1) + ".")
            print("Model identifier:")
            print(model.identifier)
            print("Model parameters:")
            pprint(model.model_parameters)
            print("Interactions:")
            print(model.interactions)
            print("Found " + str(len(model.agents)) + " agents.")
            for agent_iterator in range(0,len(model.agents)):
                print("Agent #" + str(agent_iterator+1) + ":")
                print("Identifier:")
                print(model.agents[agent_iterator].identifier)
                print("Parameters:")
                pprint(model.agents[agent_iterator].parameters)
                print("State variables:")
                pprint(model.agents[agent_iterator].state_variables)
            print("\n")
            result = model.do_update()

            self.results.append(result)
            self.write_results(model)


    def do_run_test_silent(self):
        for i in range(0, self.num_simulations):
            # generate model parameters from runner_config
            self.generate_model_config(self.model_config_template)
            self.model_config.identifier = self.model_config.identifier + "-" + str(i)

            model = Model(self.model_config)
            model.initialize_agents()
            if (model.model_parameters['R'] < 2) or (model.model_parameters['R'] > 5):
                print "ERROR in do_run: R out of bounds."
            if (model.model_parameters['beta'] < 2) or (model.model_parameters['beta'] > 5):
                print "ERROR in do_run: beta out of bounds."
            if (model.model_parameters['eta'] < 0) or (model.model_parameters['eta'] > 0.5):
                print "ERROR in do_run: eta out of bounds."
            if model.model_parameters['lambda'] != 0.5:
                print "ERROR in do_run: incorrect lambda value."
            if (model.model_parameters['phi'] < 1) or (model.model_parameters['phi'] > 2):
                print "ERROR in do_run: phi out of bounds."
            if (model.model_parameters['q'] < 0) or (model.model_parameters['q'] > 1):
                print "ERROR in do_run: q out of bounds."
            if (model.model_parameters['rho'] < 1) or (model.model_parameters['rho'] > 4):
                print "ERROR in do_run: rho out of bounds."
            if model.interactions != None:
                print "ERROR in do_run: The exist interactions."
            if len(model.agents) != self.model_config.static_parameters['num_agents']:
                print "ERROR in do_run: incorrect number of agents initialized."
            for agent_iterator in range(0,len(model.agents)):
                if model.model_parameters['q'] != model.agents[agent_iterator].parameters['q']:
                    print "ERROR in do_run: Agent initialized with q different from model"
                if model.model_parameters['rho'] != model.agents[agent_iterator].parameters['rho']:
                    print "ERROR in do_run: Agent initialized with rho different from model"
                if model.agents[agent_iterator].state_variables['b'] != [0.0,min(model.model_parameters['eta']*model.agents[agent_iterator].state_variables['d1'][1], model.agents[agent_iterator].state_variables['y'][1])]:
                    print "ERROR in do_run: Agent initialized with b different from model"
                if model.agents[agent_iterator].state_variables['d1'] != [0.1,min(model.model_parameters['R']/(model.model_parameters['lambda']+model.model_parameters['eta']), 1.5)]:
                    print "ERROR in do_run: Agent initialized with d1 different from model"
                if model.agents[agent_iterator].state_variables['y'] != [0.0,1.0]:
                    "ERROR in do_run: Agent initialized with y different from model"
            result = model.do_update()

            self.results.append(result)
            self.write_results(model)
