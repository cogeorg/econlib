#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-
from abmtemplate.baseagent import BaseAgent

class Agent(BaseAgent):
    identifier = ""
    parameters = {}
    state_variables = {}

    def get_identifier(self):
        return self.identifier
    def set_identifier(self, _value):
        super(Agent, self).set_identifier(_value)

    def get_parameters(self):
        return self.parameters
    def set_parameters(self, _value):
        super(Agent, self).set_parameters(_value)

    def get_state_variables(self):
        return self.state_variables
    def set_state_variables(self, _value):
        super(Agent, self).set_state_variables(_value)


    def __init__(self, _identifier, _params, _variables):
        super(Agent, self).__init__(_identifier, _params, _variables)
        self.utility = self.compute_utility()

    def __str__(self):
        ret_str = super(Agent, self).__str__()
        ret_str = ret_str.replace("  </agent>\n", "")  # a fix, relative to the base class, we want to also print utility
        ret_str += "    <utility value='" + str(self.utility) + "'></utility>\n"
        ret_str += "  </agent>\n"
        return ret_str


    def compute_utility(self):
        return 0.0

    def get_best_response(self, opponent_strategy):
        best_response = []

        return best_response