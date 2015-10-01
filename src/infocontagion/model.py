#!/usr/bin/env python2.7
# -*- coding: utf-8 -*-

import math

from abmtemplate.basemodel import BaseModel

from config import Config
from agent import Agent


class Model(BaseModel):
    """
    Global variables: nan
    Class variables: identifier, model_parameters, agents, interactions, steps_per_state_variable
    """
    identifier = ""
    model_parameters = {}
    agents = []
    interactions = None

    def __init__(self, model_config):
        super(Model, self).__init__(model_config)

    def get_identifier(self):
        return self.identifier
    def set_identifier(self, _value):
        """
        Class variables: identifier
        Local variables: _identifier
        """
        super(Model, self).set_identifier(_value)

    def get_model_parameters(self):
        return self.model_parameters
    def set_model_parameters(self, _value):
        """
        Class variables: model_parameters
        Local variables: _params
        """
        super(Model, self).set_model_parameters(_value)

    def get_agents(self):
        return self.agents
    def set_agents(self, _value):
        """
        Class variables: agents
        Local variables: _agents
        """
        super(Model, self).set_agents(_value)

    def get_interactions(self):
        return self.interactions
    def set_interactions(self, _value):
        """
        Class variables: interactions
        Local variables: _interactions
        """
        super(Model, self).set_interactions(_value)

    def get_agent_by_id(self, _id):
        """
        Class variables: 
        Local variables: _id
        """
        super(Model, self).get_agent_by_id(_id)

    def check_agent_homogeneity(self):
        super(Model, self).check_agent_homogeneity()        

    def __str__(self):
        """
        Class variables: identifier, model_parameters, agents, interactions
        Local variables: ret_str, entry, value, agent
        """
        return super(Model, self).__str__()


    def initialize_agents(self):
        """
        Class variables: model_parameters, agents
        Local variables: num_agents, d1_lower, d1_upper, y_lower, y_upper, b_lower, b_upper, state_variables, i, identifier, _agent
        """
        num_agents = int(self.model_parameters['num_agents'])

        # construct agent_parameters dict
        agent_parameters = {'rho': float(self.model_parameters['rho']), 'q': float(self.model_parameters['q'])}

        # TODO: these values should be set in the model config file somehow, so this code has to be refactored
        d1_lower = 0.1
        d1_upper = min(self.model_parameters['R']/(self.model_parameters['lambda']+self.model_parameters['eta']), 1.5)
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

    # -----------------------------------------------------------------------
    #
    # expected utilities
    #
    # -----------------------------------------------------------------------
    def expected_utility_A(self, agent):
        """
        Global variables: nan
        Class variables: 
        Local variables: lamb, value, agent
        """
        lamb = self.get_model_parameters()['lambda']
        value = agent.u1_A*(lamb + (1-lamb)*agent.theta_A) + (1-lamb)*(1-agent.theta_A)*0.5*(agent.u2_AG + agent.u1_A)
        if (agent.theta_A > 0.5):
            value = -nan
        return value

    def expected_utility_CE(self, agent):
        """
        Global variables: nan
        Class variables: 
        Local variables: lamb, value, state, theta_CE, q_H
        """
        value = q_H*(  theta_CE*state.u_dc + (1-theta_CE)*( lamb*state.u_d_1 + (1-lamb)*0.5*(state.u2_Gce + state.u_d_ce) )  )
        value += (1-q_H)*(lamb*state.u_d_1 + (1-lamb)*0.5*(state.u2_Gce + state.u2_Bce))
        if (theta_CE > 0.5):
            value = -nan
        return value

    def expected_utility_H(self, agent):
        """
        Global variables: nan
        Class variables: 
        Local variables: q_H, lambda_H, theta_H_bar, value, agent
        """
        q_H = self.get_model_parameters()['q']
        lambda_H = self.get_model_parameters()['lambda'] + self.get_model_parameters()['eta']
        theta_H_bar = agent.theta_H  # the bar nomenclature is outdated, but i don't want to change all the code

        value = (1.0-q_H)*(lambda_H*agent.u_d_1 + (1.0-lambda_H)*0.5*(agent.u_HG+agent.u_HB))
        value += q_H*(theta_H_bar*agent.u_d_H + lambda_H*(1.0-theta_H_bar)*agent.u_d_1)
        value += q_H*(1.0-theta_H_bar)*(1-lambda_H)*0.5*(agent.u_HG + agent.u_d_H)
        if (theta_H_bar > 0.5):
            value = -nan
        return value

    # cr
    def expected_utility_1L(self, agent):
        """
        Global variables: nan
        Class variables: 
        Local variables: a_H, q_H, q_L, lambda_L, theta_H_bar, theta_1L_bar, value, agent
        """
        # set of local parameters needed to make the computation of the value a bit less cumbersome
        q_H = self.get_model_parameters()['q']
        q_L = q_H
        lambda_L = self.get_model_parameters()['lambda'] - self.get_model_parameters()['eta']
        theta_H_bar = agent.theta_H
        theta_1L_bar = agent.theta_L
        a_H = q_H*theta_H_bar

        value = (1.0-q_L)*(  lambda_L*agent.u_d_1 + (1.0-lambda_L)*0.5*( (1.0-a_H)*(agent.u_LGN + agent.u_LBN) + a_H*(agent.u_LGD + agent.u_LGN) )  )
        value += q_L*( theta_1L_bar*((1.0-a_H)*agent.u_d_LN + a_H*agent.u_d_LD) + lambda_L*(1-theta_1L_bar)*agent.u_d_1 )
        value += q_L*(1.0-lambda_L)*0.5*( (1.0-theta_1L_bar*theta_1L_bar)*((1.0-a_H)*agent.u_LGN + a_H*agent.u_LGD) +
                                        (1.0-theta_1L_bar)*(1.0-theta_1L_bar)*((1.0-a_H)*agent.u_LBN + a_H*agent.u_LBD) )
        if ( (theta_1L_bar > 0.5) ):
            value = -nan
        return value

    # cr + ic
    def expected_utility_2L(self, agent):
        """
        Global variables: nan
        Class variables: 
        Local variables: a_H, q_H, q_L, lambda_L, theta_H_bar, theta_2LN_bar, theta_2LD_bar, value, agent
        """
        # set of local parameters needed to make the computation of the value a bit less cumbersome
        q_H = self.get_model_parameters()['q']
        q_L = q_H
        lambda_L = self.get_model_parameters()['lambda'] - self.get_model_parameters()['eta']
        theta_H_bar = agent.theta_H
        theta_2LN_bar = agent.theta_LN
        theta_2LD_bar = agent.theta_LD
        a_H = q_H*theta_H_bar

        value = (1.0-q_L)*(  lambda_L*agent.u_d_1 + (1.0-lambda_L)*0.5*((1.0-a_H)*(agent.u_LGN+agent.u_LBN)
                                                                        + a_H*(agent.u_LGD+agent.u_LBD))  )
        value += q_L*(  theta_2LN_bar*(1.0-a_H)*agent.u_d_LN + theta_2LD_bar*a_H*agent.u_d_LD
                        + lambda_L*(a_H*(1.0-theta_2LD_bar) + (1.0-a_H)*(1-theta_2LN_bar))*agent.u_d_1 )
        value += q_L*(  (1.0-lambda_L)*0.5*( (1.0-a_H)*((1.0-theta_2LN_bar*theta_2LN_bar)*agent.u_LGN
                                                        + (1.0-theta_2LN_bar)*(1.0-theta_2LN_bar)*agent.u_LBN)
                                             + a_H*((1.0-theta_2LD_bar*theta_2LD_bar)*agent.u_LGD
                                                    + (1-theta_2LD_bar)*(1-theta_2LD_bar)*agent.u_LBD) )  )
        if ( (theta_2LN_bar > 0.5) or (theta_2LD_bar > 0.5) ):
            value = -nan
        return value

    # ce
    def expected_utility_5(self, agent):
        """
        Global variables: nan
        Class variables: 
        Local variables: q_H, q_L, lamb, theta_bar, value, agent
        """
        # set of local parameters needed to make the computation of the value a bit less cumbersome
        q_H = self.get_model_parameters()['q']
        q_L = q_H
        lamb = self.get_model_parameters()['lambda']
        theta_bar = agent.theta

        value = 0.5*(q_H + q_L)*(  theta_bar*agent.u_dc + (1.0-theta_bar)*(lamb*agent.u_d_1
                                                                           + (1.0-lamb)*0.5*(agent.u_Gc + agent.u_dc) )  )
        value += 0.5*(1.0-q_H + 1.0-q_L)*( lamb*agent.u_d_1 + (1.0-lamb)*0.5*(agent.u_Gc + agent.u_Bc) )
        if (theta_bar > 0.5):
            value = -nan
        return value

    # ce + ic
    def expected_utility_6(self, agent):
        """
        Global variables: nan
        Class variables: 
        Local variables: q_H, q_L, lamb, theta_bar, value, agent
        """
        # set of local parameters needed to make the computation of the value a bit less cumbersome
        q_H = self.get_model_parameters()['q']
        q_L = q_H
        lamb = self.get_model_parameters()['lambda']
        theta_bar = agent.theta

        value = (q_H + q_L - q_H*q_L)*(  theta_bar*agent.u_dc
                                         + (1.0-theta_bar)*(lamb*agent.u_d_1 + 0.5*(1.0-lamb)*(agent.u_Gc + agent.u_dc) )  )
        value += (1.0-q_H)*(1.0-q_L)*( lamb*agent.u_d_1 + (1.0-lamb)*0.5*(agent.u_Gc + agent.u_Bc) )

        if (theta_bar > 0.5):
            value = -nan

        return value

    # -----------------------------------------------------------------------

    def calculate_EUA(self, agent):
        """
        Class variables: 
        Local variables: EUA, agent
        """
        EUA = self.expected_utility_A(agent)
        return EUA

    def calculate_EUCE(self, agent):
        """
        Class variables: 
        Local variables: EUCE, agent
        """
        EUCE = self.expected_utility_CE(agent)
        return EUCE

    def calculate_EU1(self, agent):
        """
        Class variables: 
        Local variables: EU1_H, EU1_L, EU1, agent
        """
        EU1_H = self.expected_utility_H(agent)
        EU1_L = self.expected_utility_1L(agent)
        EU1 = 0.5*(EU1_H + EU1_L)
        return EU1

    def calculate_EU2(self, agent):
        """
        Class variables: 
        Local variables: theta_2LN_bar, theta_2LD_bar, EU2, EU_H, EU2_L, agent
        """
        theta_2LN_bar = agent.theta_LN
        theta_2LD_bar = agent.theta_LD
        if (theta_2LN_bar > theta_2LD_bar):
            EU2 = -nan
        else:
            EU_H = self.expected_utility_H(agent)
            EU2_L = self.expected_utility_2L(agent)
            EU2 = 0.5*(EU_H + EU2_L)
        return EU2

    def calculate_EU5(self, agent):
        """
        Class variables: 
        Local variables: agent
        """
        return self.expected_utility_5(agent)

    def calculate_EU6(self, agent):
        """
        Class variables: 
        Local variables: agent
        """
        return self.expected_utility_6(agent)
    
    def calculate_EU_test(self, agent):
        """
        Class variables: 
        Local variables: EU1, agent
        """
        EU1 = agent.state_variables['d1'] + agent.state_variables['y'] - agent.state_variables['b']
        return EU1

    # -----------------------------------------------------------------------
    #
    # find_optimum
    #
    # -----------------------------------------------------------------------
    def find_optimum(self, agent):
        """
        Global variables: nan
        Class variables: 
        Local variables: agent, d1, d1_lower, d1_upper, step_d1, y, y_lower, y_upper, step_y,
        Local variables: b, b_lower, b_upper, step_b, maxA, max1, max2, max5, max6, EUA, EU1, EU2, EU5, EU6
        """
        global nan
        nan = 10000000000000000.0

        d1 = agent.state_variables['d1']
        d1_lower = float(d1[0])
        d1_upper = float(d1[1])
        step_d1 = (d1_upper - d1_lower)/self.steps_per_state_variable

        y = agent.state_variables['y']
        y_lower = float(y[0])
        y_upper = float(y[1])
        step_y = (y_upper - y_lower)/self.steps_per_state_variable

        b = agent.state_variables['b']
        b_lower = float(b[0])
        b_upper = float(b[1])
        step_b = (b_upper - b_lower)/self.steps_per_state_variable

        maxA = [-nan, d1_lower, y_lower, b_lower]
        max1 = [-nan, d1_lower, y_lower, b_lower]
        max2 = [-nan, d1_lower, y_lower, b_lower]
        max5 = [-nan, d1_lower, y_lower, b_lower]
        max6 = [-nan, d1_lower, y_lower, b_lower]

        d1 = d1_lower
        while d1 <= d1_upper:
            y = y_lower
            while y <= y_upper:
                b = b_lower
                while b <= b_upper:
                    # first set agentA state variables
                    agent.set_state_variables({'d1': d1, 'y': y, 'b': b})
                    agent.compute_ancillary_variables(self.model_parameters['R'],
                                                      self.model_parameters['beta'],
                                                      self.model_parameters['lambda'],
                                                      self.model_parameters['phi'],
                                                      self.model_parameters['eta'])

                    # - we have to compute 4 different cases: cr, cr+ic, ce, ce+ic, and evaluate cr+ic and ce+ic at
                    #   their optimal contract as well as at the contract of cr and ce, respectively.
                    # - it is more efficient to compute all six expected utilities at once and store the optimum of
                    #   the state variables in an array of optimum variables

                    EUA = self.calculate_EUA(agent)
                    if (EUA > maxA[0]):
                        maxA = [EUA, d1, y, b]

                    EU1 = self.calculate_EU1(agent)
                    if (EU1 > max1[0]):
                        max1 = [EU1, d1, y, b]

                    EU2 = self.calculate_EU2(agent)
                    if (EU2 > max2[0]):
                        max2 = [EU2, d1, y, b]

                    EU5 = self.calculate_EU5(agent)
                    if (EU5 > max5[0]):
                        max5 = [EU5, d1, y, b]

                    EU6 = self.calculate_EU6(agent)
                    if (EU6 > max6[0]):
                        max6 = [EU6, d1, y, b]

                    # increase b
                    b += step_b
                # increase y
                y += step_y
            # increase d1
            d1 += step_d1
        return([max1, max2, max5, max6])

    # =======================================================================
    # do_update
    # =======================================================================
    def do_update(self):
        """
        Class variables: agents, steps_per_state_variable
        Local variables: agent, optimum
        """
        # equilibrium is symmetric, i.e. we only require one agent
        agent = self.agents[0]

        self.steps_per_state_variable = int(round(math.pow(float(self.model_parameters['num_sweeps']),
                                                           1.0/len(agent.state_variables)), 0))

        optimum = self.find_optimum(agent)
        return optimum