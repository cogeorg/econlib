#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import math

from abmtemplate.basemodel import BaseModel

from config import Config
from agent import Agent


class Model(BaseModel):
    identifier = ""
    model_parameters = {}
    agents = []
    interactions = None

    def __init__(self, model_config):
        super(Model, self).__init__(model_config)

    def get_identifier(self):
        return self.identifier
    def set_identifier(self, _value):
        super(Model, self).set_identifier(_value)

    def get_model_parameters(self):
        return self.model_parameters
    def set_model_parameters(self, _value):
        super(Model, self).set_model_parameters(_value)

    def get_agents(self):
        return self.agents
    def set_agents(self, _value):
        super(Model, self).set_agents(_value)

    def get_interactions(self):
        return self.interactions
    def set_interactions(self, _value):
        super(Model, self).set_interactions(_value)

    def __str__(self):
        return super(Model, self).__str__()


    def initialize_agents(self):
        num_agents = int(self.model_parameters['num_agents'])

        # construct agent_parameters dict
        agent_parameters = {'rho': float(self.model_parameters['rho'])}

        # TODO: these values should be set in the model config file somehow, so this code has to be refactored
        d1_lower = 0.1
        d1_upper = min(self.model_parameters['RG']/(self.model_parameters['lambda']+self.model_parameters['eta']), 1.5)
        y_lower = 0.0
        y_upper = 1.0
        b_lower = 0.0
        b_upper = min(self.model_parameters['eta']*d1_upper, y_upper)
        state_variables = {'d1': [d1_lower, d1_upper], 'y': [y_lower, y_upper], 'b': [b_lower, b_upper]}

        # create agents and append them to the array of agents
        for i in range(0, num_agents):
            identifier = str(i)
            _agent = Agent(identifier, agent_parameters, state_variables)
            self.agents.append(_agent)

    def get_agent_by_id(self, _id):
        for agent in self.agents
            if agent.identifier == _id:
                return agent

    def check_agent_homogeneity(self):
        for entry in self.agents[0].parameters:
            check_param = self.agents[0].parameters[entry]
            for agent in self.agents:
                if agent.parameters[entry] != check_param:
                    return False
                check_param = agent.parameters[entry]
        for entry in self.agents[0].state_variables:
            check_stvar = self.agents[0].state_variables[entry]
            for agent in self.agents:
                if agent.state_variables[entry] != check_stvar:
                    return False
                check_stvar == agent.state_variables[entry]
        return True

    # TODO make this into a recursive routine that iterates automatically through all agentA.state_variables
    def compute_equilibrium(self, agentA, agentB):
        d1 = agentA.state_variables['d1']
        d1_lower = float(d1[0])
        d1_upper = float(d1[1])
        step_d1 = (d1_upper - d1_lower)/self.steps_per_state_variable

        y = agentA.state_variables['y']
        y_lower = float(y[0])
        y_upper = float(y[1])
        step_y = (y_upper - y_lower)/self.steps_per_state_variable

        b = agentA.state_variables['b']
        b_lower = float(b[0])
        b_upper = float(b[1])
        step_b = (b_upper - b_lower)/self.steps_per_state_variable

        precision = 0.01

        d1_A = d1_lower
        while d1_A <= d1_upper:
            y_A = y_lower
            while y_A <= y_upper:
                b_A = b_lower
                while b_A <= b_upper:
                    # first set agentA state variables
                    agentA.state_variables = {'d1': d1_A, 'y': y_A, 'b': b_A}

                    # then get the best response of B given the current portfolio choice of A
                    ret_B = agentB.get_best_response([d1_A, y_A, b_A])

                    # and then get the best response of A given the best response of B
                    ret_A = agentA.get_best_response([ret_B[0], ret_B[1], ret_B[2]])

                    # check if we have a fixed point
                    if ( abs(ret_A[0] - d1_A) < precision) and (abs(ret_A[1] - y_A) < precision) and (abs(ret_A[2] - b_A) < precision):
                        # here we have to write out the results
                        pass
                    # increase b_A
                    b_A += step_b
                # increase y_A
                y_A += step_y
            # increase d1_A
            d1_A += step_d1

    def compute_equilibrium_recursive(self, agentA, agentB):
        self.par_keys = []
        self.par_lower = []
        self.par_upper = []
        self.par_step  = []
        self.par_current = []
        for state_key, state_var in agentA.state_variables:
            self.par_keys.append(str(state_key))
            self.par_lower.append(float(state_var[0]))
            self.par_upper.append(float(state_var[1]))
            self.par_step.append((self.par_upper[-1] - self.par_lower[-1])/self.steps_per_state_variable)
        
        self.precision = 0.01
        self.par_current = self.par_lower
        self.loop_over_dimension(0)

    def loop_over_dimension(self,p_step):
        while self.par_current[p_step] <= self.par_upper[p_step]:
            if (p_step+2) < len(self.par_upper):
                self.loop_over_dimension(p_step+1)
            elif (p_step+1) == len(self.par_upper):
                # first set agentA state variables
                for state_iterator in range(0,len(self.par_keys)):
                    agentA.state_variables[self.state_key[state_iterator]] = self.par_current[state_iterator]

                # then get the best response of B given the current portfolio choice of A
                ret_B = agentB.get_best_response(self.par_current)

                # and then get the best response of A given the best response of B
                ret_A = agentA.get_best_response(ret_B)

                # check if we have a fixed point
                #if ( abs(ret_A[0] - d1_A) < precision) and (abs(ret_A[1] - y_A) < precision) and (abs(ret_A[2] - b_A) < precision):
                if all(i < self.precision for i in [abs(x) - y for x, y in zip(ret_A, self.par_current)])
                    # here we have to write out the results
                    pass
            self.par_current[p_step] += self.par_step[p_step]

    def do_update(self):
        # equilibrium is found by iterating over all possible variable choices for agent A, communicating them to
        # agent B, obtaining B's best response by iterating over all possible variable choices for B, communicating
        # B's best response back to A, and computing A's best response. Any fixed point of this procedure is an
        # equilibrium
        agentA = self.agents[0]
        agentB = self.agents[1]

        self.steps_per_state_variable = math.pow(float(self.model_parameters['num_sweeps']),1.0/len(agentA.state_variables))
        self.compute_equilibrium(agentA, agentB)

        # we need the stepwidth
        #print self.model_parameters
        #print agentA.state_variables.keys(), agentA.state_variables
