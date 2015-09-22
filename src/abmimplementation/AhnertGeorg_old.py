#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__="""Co-Pierre Georg (cogeorg@gmail.com)"""


#============================================================================
class Model(object):
    #============================================================================
    #
    # VARIABLES
    #


    #
    # METHODS
    #
    #============================================================================
    # __init__
    #============================================================================
    def __init__(self):
        pass

    #============================================================================
    # utility(consumption)
    #============================================================================
    def utility(self, consumption):
        import math

        if (consumption < 0.0):
            #print "ERROR: consumption negative: " + str(consumption)
            return -nan
        else:
            if (rho == 0.0): # just for debugging
                value = consumption
            if (rho == 1.0): # just for debugging
                try:
                    value = math.log(consumption)
                except:
                    value = -nan
            else:
                # CRRA with rho > 1.0 produces negative utility for consumption < 1.0
                try:
                    value = (pow(consumption,(1.0-rho)))/(1.0-rho)
                #print value
                except:
                    value = -nan

        return value
    #============================================================================

#============================================================================


#============================================================================
class State(object):
    #============================================================================
    #
    # VARIABLES
    #
    d_1 = 0.0
    y = 0.0
    b = 0.0

    # for autarky and competitive equilibrium
    c1_A = 0.0
    c2_AB = 0.0
    c2_AG = 0.0
    d_ce = 0.0
    c2_Gce = 0.0
    c2_Bce = 0.0

    u1_A = 0.0
    u2_AB = 0.0
    u2_AG = 0.0
    u_d_ce = 0.0
    u2_Gce = 0.0
    u2_Bce = 0.0

    # for cases 1-6
    d_H = 0.0
    c_HB = 0.0
    c_HG = 0.0

    u_HB = 0.0
    u_HG = 0.0
    u_d_H = 0.0
    u_d_1 = 0.0

    #
    # REGION L
    #
    d_LN = 0.0
    d_LD = 0.0
    c_LGN = 0.0
    c_LGD = 0.0
    c_LBN = 0.0
    c_LBD = 0.0

    u_LGN = 0.0
    u_LGD = 0.0
    u_LBN = 0.0
    u_LBD = 0.0
    u_d_LN = 0.0
    u_d_LD = 0.0

    #
    # PURE INTERBANK CONTAGION
    #
    dc = 0.0
    c_Gc = 0.0
    c_Bc = 0.0

    u_dc = 0.0
    u_Gc = 0.0
    u_Bc = 0.0


    #
    # METHODS
    #
    #============================================================================
    # __init__
    #============================================================================
    def __init__(self):
        pass
    #============================================================================

    #============================================================================
    # recalculate()
    #============================================================================
    def recalculate(self, d_1,y,b):
        model = Model()
        self.d_1 = d_1
        self.y = y
        self.b = b

        #
        # calculate variables for autarky and comp. eq.
        #
        self.c1_A = y + (1-y)*beta
        self.c2_AB = y
        self.c2_AG = y + (1-y)*R
        self.u1_A = model.utility(self.c1_A)
        self.u2_AB = model.utility(self.c2_AB)
        self.u2_AG = model.utility(self.c2_AG)

        self.d_ce = y + (1.0-y)*beta
        self.c2_Gce = (y-lamb*d_1 + (1.0-y)*R)/(1.0-lamb)
        self.c2_Bce = (y-lamb*d_1)/(1.0-lamb)
        self.u_d_ce = model.utility(self.d_ce)
        self.u2_Gce = model.utility(self.c2_Gce)
        self.u2_Bce = model.utility(self.c2_Bce)

        #
        # now recalculate all values with the optimal values for (d_1,b,y)
        #
        self.d_H = y + beta*(1.0-y) + b
        self.c_HB = (y-lambda_H*d_1-(phi-1.0)*b)/(1.0-lambda_H)
        self.c_HG = (R*(1.0-y)+y-lambda_H*d_1-(phi-1.0)*b)/(1.0-lambda_H)

        self.u_HB = model.utility(self.c_HB)
        self.u_HG = model.utility(self.c_HG)
        self.u_d_H = model.utility(self.d_H)
        self.u_d_1 = model.utility(d_1)
        #print str(u_HB) + " " + str(u_HG) + " " + str(d_H) + " " + str(u_d_1)
        #print str(u_d_H - u_HB) + " " + str(u_HG - u_HB)

        #
        # REGION L
        #
        self.d_LN = y+beta*(1.0-y)+b*(beta*phi-1.0)
        self.d_LD = y+beta*(1.0-y)-b
        self.c_LGN = (R*(1.0-y)+y-lambda_L*d_1+(phi-1.0)*b)/(1.0-lambda_L)
        self.c_LGD = (R*(1.0-y)+y-lambda_L*d_1-b)/(1.0-lambda_L)
        self.c_LBN = (y-lambda_L*d_1+(phi-1.0)*b)/(1.0-lambda_L)
        self.c_LBD = (y-lambda_L*d_1-b)/(1.0-lambda_L)
        #print str(d_LN) + " " + str(d_LD) + " " + str(c_LGN) + " " + str(c_LGD) + " " + str(c_LBN) + " " + str(c_LBD)

        self.u_LGN = model.utility(self.c_LGN)
        self.u_LGD = model.utility(self.c_LGD)
        self.u_LBN = model.utility(self.c_LBN)
        self.u_LBD = model.utility(self.c_LBD)
        self.u_d_LN = model.utility(self.d_LN)
        self.u_d_LD = model.utility(self.d_LD)
        #print str(u_LGN) + " " + str(u_LGD) + " " + str(u_LBN) + " " + str(u_LBD) + " " + str(u_d_LN) + " " + str(u_d_LD)

        # Pure common shock
        self.dc = y + (1-y)*beta
        self.c_Gc = ((1.0-y)*R + y - lamb*d_1)/(1.0-lamb)
        self.c_Bc = (y-lamb*d_1)/(1.0-lamb)

        self.u_dc = model.utility(self.dc)
        self.u_Gc = model.utility(self.c_Gc)
        self.u_Bc = model.utility(self.c_Bc)
    #------------------------------------------------------------------------
#============================================================================


#============================================================================
# calculate_theta_A()
#============================================================================
def calculate_theta_A(state):
    try:
        value = (state.u1_A-state.u2_AB)/(state.u2_AG-state.u2_AB)
    except:
        value = 0.0

    if (value < 0.0):
        value = 0.0
    if (value > 0.5):
        value = 0.5

    return value
#============================================================================


#============================================================================
# calculate_theta_CE()
#============================================================================
def calculate_theta_CE(state):
    try:
        value = (state.u_d_ce - state.u2_Bce)/(state.u2_Gce - state.u2_Bce)
    except:
        value = 0.0

    if (value < 0.0):
        value = 0.0
    if (value > 1.0):
        value = 1.0

    return value
#============================================================================



#============================================================================
# calculate_theta_H()
#============================================================================
def calculate_theta_H(state):
    #print str(state.u_d_H) + " - " + str(state.u_HB) + " / " + str(state.u_HG) + " - " + str(state.u_HB)

    try:
        value = (state.u_d_H-state.u_HB)/(state.u_HG-state.u_HB)
    except:
        value = 0.0

    if (value < 0.0):
        value = 0.0
    if (value > 0.5):
        value = 0.5

    #print value

    return value
#============================================================================


#============================================================================
# calculate_theta_L()
#============================================================================
def calculate_theta_L(state, a_H):
    try:
        value = (a_H*(state.u_d_LD-state.u_LBD) + (1.0-a_H)*(state.u_d_LN-state.u_LBN)) / (a_H*(state.u_LGD-state.u_LBD) + (1.0-a_H)*(state.u_LGN-state.u_LBN))
    except:
        value = 0.0

    if (value < 0.0):
        value = 0.0
    if (value > 0.5):
        value = 0.5

    return value
#============================================================================


#============================================================================
# calculate_theta_LN(state)
#============================================================================
def calculate_theta_LN(state):
    try:
        value = (state.u_d_LN - state.u_LBN) / (state.u_LGN - state.u_LBN)
    except:
        value = 0.0

    if (value < 0.0):
        value = 0.0
    if (value > 0.5):
        value = 0.5

    return value
#============================================================================


#============================================================================
# calculate_theta_LD()
#============================================================================
def calculate_theta_LD(state):
    try:
        value = (q_H*(state.u_d_LD - state.u_LBD) + (1.0 - q_H)*(state.u_d_LN - state.u_LBN) ) / (q_H*(state.u_LGD - state.u_LBD) + (1.0 - q_H)*(state.u_LGN - state.u_LBN) )
    except:
        value = 0.0

    if (value < 0.0):
        value = 0.0
    if (value > 0.5):
        value = 0.5

    return value
#============================================================================


#============================================================================
# calculate_theta
#============================================================================
def calculate_theta(state):
    try:
        value = (state.u_dc - state.u_Bc)/(state.u_Gc - state.u_Bc)
    except:
        value = 0.0

    if (value < 0.0):
        value = 0.0
    if (value > 0.5):
        value = 0.5

    return value
#============================================================================


#============================================================================
# expected_utility_A
#============================================================================
def expected_utility_A(state,  theta_A):
    value = state.u1_A*(lamb + (1-lamb)*theta_A) + (1-lamb)*(1-theta_A)*0.5*(state.u2_AG + state.u1_A)

    if (theta_A > 0.5):
        value = -nan

    return value
#============================================================================


#============================================================================
# expected_utility_CE
#============================================================================
def expected_utility_CE(state,  theta_CE,  debug):
    value = q_H*(  theta_CE*state.u_dc + (1-theta_CE)*( lamb*state.u_d_1 + (1-lamb)*0.5*(state.u2_Gce + state.u_d_ce) )  )
    value += (1-q_H)*(lamb*state.u_d_1 + (1-lamb)*0.5*(state.u2_Gce + state.u2_Bce))

    if (debug):
        print str(state.d_1) + " " + str(state.y) + " " + str(lamb) + " | " + str(state.u_d_ce) + " " + str(state.u_d_1) + " " + str(state.u2_Gce) + " " + str(state.u2_Bce) + " | " + str(theta_CE) + " " + str(value)


    if (theta_CE > 0.5):
        value = -nan

    return value
#============================================================================


#============================================================================
# expected_utility_H
#============================================================================
def expected_utility_H(state,  theta_H_bar):
    value = (1-q_H)*(lambda_H*state.u_d_1 + (1-lambda_H)*0.5*(state.u_HG+state.u_HB))
    value += q_H*(theta_H_bar*state.u_d_H + lambda_H*(1-theta_H_bar)*state.u_d_1)
    value += q_H*(1-lambda_H)*0.5*((1-theta_H_bar*theta_H_bar)*state.u_HG + (1-theta_H_bar)*(1-theta_H_bar)*state.u_HB)

    if (theta_H_bar > 0.5):
        value = -nan

    return value
#============================================================================


#============================================================================
# expected_utility_1L
#============================================================================
def expected_utility_1L(state,  theta_1L_bar):
    value = (1-q_L)*(  lambda_L*state.u_d_1 + (1-lambda_L)*0.5*( (1-a_H)*(state.u_LGN + state.u_LGD) + a_H*(state.u_LGN + state.u_LGD) )  )
    value += q_L*( theta_1L_bar*((1-a_H)*state.u_d_LN + a_H*state.u_d_LD) + lambda_L*(1-theta_1L_bar)*state.u_d_1 )
    value += q_L*(1-lambda_L)*0.5*( (1-theta_1L_bar*theta_1L_bar)*((1-a_H)*state.u_LGN + a_H*state.u_LGD) + (1-theta_1L_bar)*(1-theta_1L_bar)*((1-a_H)*state.u_LBN + a_H*state.u_LBD) )

    if ( (theta_1L_bar > 0.5) ):
        value = -nan

    return value
#============================================================================


#============================================================================
# expected_utility_2L
#============================================================================
def expected_utility_2L(state, theta_2LN_bar,  theta_2LD_bar):
    value = (1-q_L)*(  lambda_L*state.u_d_1 + (1-lambda_L)*0.5*((1-a_H)*(state.u_LGN+state.u_LBN) + a_H*(state.u_LGD+state.u_LBD))  )
    value += q_L*(  theta_2LN_bar*(1-a_H)*state.u_d_LN + theta_2LD_bar*a_H*state.u_d_LD + lambda_L*(a_H*(1-theta_2LD_bar) + (1-a_H)*(1-theta_2LN_bar))*state.u_d_1 )
    value += q_L*(  (1-lambda_L)*0.5*( (1-a_H)*((1-theta_2LN_bar*theta_2LN_bar)*state.u_LGN + (1-theta_2LN_bar)*(1-theta_2LN_bar)*state.u_LBN) + a_H*((1-theta_2LD_bar*theta_2LD_bar)*state.u_LGD + (1-theta_2LD_bar)*(1-theta_2LD_bar)*state.u_LBD) )  )

    if ( (theta_2LN_bar > 0.5) or (theta_2LD_bar > 0.5) ):
        value = -nan

    return value
#============================================================================


#============================================================================
# expected_utility_3u
#============================================================================
def expected_utility_3u(state,  theta_H_bar):
    # EU3_u_1
    value = (1-q_L)*(1-q_H)*0.5*(  2*lamb*state.u_d_1 + (1-lambda_L)*0.5*(state.u_LGN + state.u_LBN) + (1-lambda_H)*0.5*(state.u_HG + state.u_HB) )

    # EU3_u_2
    value += (1-q_L)*q_H*0.5*(  theta_H_bar*(state.u_d_H + lambda_L*state.u_d_1) + (1-lambda_L)*theta_H_bar*(state.u_LBD + 0.5*theta_H_bar*(state.u_LGD - state.u_LBD) )  )
    value += (1-q_L)*q_H*0.5*(  (1-theta_H_bar)*2*lamb*state.u_d_1 + (1-lambda_L)*0.5*((1-theta_H_bar*theta_H_bar)*state.u_LGN + (1-theta_H_bar)*(1-theta_H_bar)*state.u_LBN )  )
    value += (1-q_L)*q_H*0.5*(  (1-lambda_H)*0.5*( (1-theta_H_bar*theta_H_bar)*state.u_HG + (1-theta_H_bar)*(1-theta_H_bar)*state.u_HB )  )

    if ( (theta_H_bar > 0.5) ):
        value = -nan

    return value
#============================================================================


#============================================================================
# expected_utility_3i1
#============================================================================
def expected_utility_3i1(state,  theta_H_bar,  theta_2LN_bar,  theta_2LD_bar):
    value = q_L*0.5*( theta_H_bar*(q_H*(state.u_d_H + state.u_d_LD)+(1-q_H)*(state.u_d_LN+lambda_H*state.u_d_1+(1-lambda_H)*(state.u_HB + 0.5*theta_H_bar*(state.u_HG - state.u_HB))) )  )
    value += q_L*0.5*(  (theta_2LN_bar-theta_H_bar)*(lambda_H*state.u_d_1 + (1-lambda_H)*(state.u_HB + 0.5*(theta_2LN_bar+theta_H_bar)*(state.u_HG-state.u_HB)) + state.u_d_LN )  )
    value += q_L*0.5*(  (1-theta_2LN_bar)*2*lamb*state.u_d_1 + (1-lambda_H)*0.5*( (1-theta_2LN_bar*theta_2LN_bar)*state.u_HG + (1-theta_2LN_bar)*(1-theta_2LN_bar)*state.u_HB ) + (1-lambda_L)*0.5*( (1-theta_2LN_bar*theta_2LN_bar)*state.u_LGN + (1-theta_2LN_bar)*(1-theta_2LN_bar)*state.u_LBN )  )

    if ( (theta_H_bar > 0.5) or (theta_2LN_bar > 0.5) or (theta_2LD_bar > 0.5) ):
        value = -nan

    return value
#============================================================================


#============================================================================
# expected_utility_3i2
#============================================================================
def expected_utility_3i2(state,  theta_H_bar):
    value = theta_H_bar*( q_H*(state.u_d_H + state.u_d_LD) + (1-q_H)*(state.u_d_LN + lambda_H*state.u_d_1 + (1-lambda_H)*(state.u_HB + 0.5*theta_H_bar*(state.u_HG - state.u_HB))) )
    value += (1-theta_H_bar)*2*lamb*state.u_d_1 + (1-lambda_H)*0.5*((1-theta_H_bar*theta_H_bar)*state.u_HG + (1-theta_H_bar)*(1-theta_H_bar)*state.u_HB) + (1-lambda_L)*0.5*((1-theta_H_bar*theta_H_bar)*state.u_LGN + (1-theta_H_bar)*(1-theta_H_bar)*state.u_LBN)

    value = value*q_L*0.5

    if (theta_H_bar > 0.5):
        value = -nan

    return value
#============================================================================


#============================================================================
# expected_utility_3i3
#============================================================================
def expected_utility_3i3(state,  theta_H_bar,  theta_2LN_bar,  theta_2LD_bar):
    value = theta_2LN_bar*(q_H*(state.u_d_H+state.u_d_LD) + (1-q_H)*(lambda_H*state.u_d_1 + state.u_d_LN) )
    value += (1-q_H)*theta_2LN_bar*(1-lambda_H)*(state.u_HB + theta_2LN_bar*(state.u_HG - state.u_HB))
    value += (theta_2LD_bar-theta_2LN_bar)*( q_H*(state.u_d_H+state.u_d_LD) + (1-q_H)*2*lamb*state.u_d_1 )
    value += (1-q_H)*(theta_2LD_bar-theta_2LN_bar)*(  (1-lambda_H)*(state.u_HB + 0.5*(theta_2LD_bar+theta_2LN_bar)*(state.u_HG-state.u_HB) + (1-lambda_L)*(state.u_LBN + 0.5*(theta_2LN_bar+theta_2LD_bar)*(state.u_LGN-state.u_LBN)) )  )
    value += q_H*(theta_H_bar-theta_2LD_bar)*(state.u_d_H + lambda_L*state.u_d_1 + (1-lambda_L)*(state.u_LBD + 0.5*(theta_H_bar+theta_2LD_bar)*(state.u_LGD-state.u_LBD) ) )
    value += (1-q_H)*(theta_H_bar-theta_2LD_bar)*( 2*lamb*state.u_d_1 + (1-lambda_H)*(state.u_HB + 0.5*(theta_H_bar+theta_2LD_bar)*(state.u_HG-state.u_HB)) + (1-lambda_L)*(state.u_LBN + 0.5*(theta_H_bar+theta_2LD_bar)*(state.u_LGN - state.u_LBN) )  )
    value += (1-theta_H_bar)*2*lamb*state.u_d_1 + (1-lambda_H)*0.5*( (1-theta_H_bar*theta_H_bar)*state.u_HG + (1-theta_H_bar)*(1-theta_H_bar)*state.u_HB) + (1-lambda_L)*0.5*( (1-theta_H_bar*theta_H_bar)*state.u_LGN + (1-theta_H_bar)*(1-theta_H_bar)*state.u_LBN )

    value = value*q_L*0.5

    if ( (theta_H_bar > 0.5) or (theta_2LN_bar > 0.5) or (theta_2LD_bar > 0.5) ):
        value = -nan

    return value
#============================================================================


#============================================================================
# expected_utility_4u
#============================================================================
def expected_utility_4u(state):
    value = (1-q_L)*(1-q_H)*0.5*(2*lamb*state.u_d_1 + 0.5*(1-lambda_H)*(state.u_HG + state.u_HB) + 0.5*(1-lambda_L)*(state.u_LGN + state.u_LBN) )

    return value
#============================================================================


#============================================================================
# expected_utility_4i1
#============================================================================
def expected_utility_4i1(state,  theta_H_bar,  theta_2LN_bar,  theta_2LD_bar):
    value = theta_H_bar*(state.u_d_LD + state.u_d_H) + (theta_2LN_bar-theta_H_bar)*(lambda_H*state.u_d_1 + state.u_d_LN)
    value += (1-lambda_H)*(theta_2LN_bar-theta_H_bar)*(state.u_HB + 0.5*(theta_2LN_bar+theta_H_bar)*(state.u_HG-state.u_HB))
    value += (1-theta_2LN_bar)*2*lamb*state.u_d_1 + (1-lambda_H)*0.5*((1-theta_2LN_bar*theta_2LN_bar)*state.u_HG + (1-theta_2LN_bar)*(1-theta_2LN_bar)*state.u_HB)
    value += (1-lambda_L)*0.5*((1-theta_2LN_bar*theta_2LN_bar)*state.u_LGN + (1-theta_2LN_bar)*(1-theta_2LN_bar)*state.u_LBN)

    value = value*(q_L + (1-q_L)*q_H)*0.5

    if ( (theta_H_bar > 0.5) or (theta_2LN_bar > 0.5) or (theta_2LD_bar > 0.5) ):
        value = -nan

    return value
#============================================================================


#============================================================================
# expected_utility_4i2
#============================================================================
def expected_utility_4i2(state,  theta_H_bar):
    value = theta_H_bar*(state.u_d_LD + state.u_d_H) + (1-theta_H_bar)*2*lamb*state.u_d_1
    value += (1-lambda_H)*0.5*((1-theta_H_bar*theta_H_bar)*state.u_HG + (1-theta_H_bar)*(1-theta_H_bar)*state.u_HB)
    value += (1-lambda_L)*0.5*((1-theta_H_bar*theta_H_bar)*state.u_LGN + (1-theta_H_bar)*(1-theta_H_bar)*state.u_LBN)

    value = value*(q_L + (1-q_L)*q_H)*0.5

    if (theta_H_bar > 0.5):
        value = -nan

    return value
#============================================================================


#============================================================================
# expected_utility_4i3
#============================================================================
def expected_utility_4i3(state,  theta_H_bar,  theta_2LN_bar,  theta_2LD_bar):
    value = theta_2LD_bar*(state.u_d_LD + state.u_d_H) + (theta_H_bar - theta_2LD_bar)*(state.u_d_H + lambda_L*state.u_d_1)
    value += (1-lambda_L)*(theta_H_bar-theta_2LD_bar)*(state.u_LBD + 0.5*(theta_H_bar+theta_2LD_bar)*(state.u_LGD - state.u_LBD))
    value += (1-theta_H_bar)*2*lamb*state.u_d_1 + (1-lambda_H)*0.5*((1-theta_H_bar*theta_H_bar)*state.u_HG + (1-theta_H_bar)*(1-theta_H_bar)*state.u_HB)
    value += (1-lambda_L)*0.5*((1-theta_H_bar*theta_H_bar)*state.u_LGN + (1-theta_H_bar)*(1-theta_H_bar)*state.u_LBN)

    value = value*(q_L + (1-q_L)*q_H)*0.5

    if ( (theta_H_bar > 0.5) or (theta_2LN_bar > 0.5) or (theta_2LD_bar > 0.5) ):
        value = -nan

    return value
#============================================================================


#============================================================================
# expected_utility_5
#============================================================================
def expected_utility_5(state,  theta_bar):
    value = 0.5*(q_H + q_L)*(  theta_bar*state.u_dc + (1-theta_bar)*(lamb*state.u_d_1 + (1-lamb)*0.5*(state.u_Gc + state.u_dc) )  )
    value += 0.5*(1-q_H + 1-q_L)*( lamb*state.u_d_1 + (1-lamb)*0.5*(state.u_Gc + state.u_Bc) )

    if (theta_bar > 0.5):
        value = -nan

    return value
#============================================================================


#============================================================================
# expected_utility_6
#============================================================================
def expected_utility_6(state,  theta_bar):
    value = (q_H + q_L - q_H*q_L)*(  theta_bar*state.u_dc + (1-theta_bar)*(lamb*state.u_d_1 + 0.5*(1-lamb)*(state.u_Gc + state.u_dc) )  )
    value += (1-q_H)*(1-q_L)*( lamb*state.u_d_1 + (1-lamb)*0.5*(state.u_Gc + state.u_Bc) )

    if (theta_bar > 0.5):
        value = -nan

    return value
#============================================================================


#============================================================================
# calculate_EUA(state)
#============================================================================
def calculate_EUA(state,  theta_A):
    EUA = expected_utility_A(state,  theta_A)
    return EUA
#============================================================================


#============================================================================
# calculate_EUCE(state)
#============================================================================
def calculate_EUCE(state,  theta_CE,  debug):
    EUCE = expected_utility_CE(state,  theta_CE,  debug)
    return EUCE
#============================================================================


#============================================================================
# calculate_EU1(state)
#============================================================================
def calculate_EU1(state,  theta_H_bar,  theta_1L_bar):
    EU1_H = expected_utility_H(state,  theta_H_bar)
    EU1_L = expected_utility_1L(state, theta_1L_bar)
    EU1 = 0.5*(EU1_H + EU1_L)

    return EU1
#============================================================================


#============================================================================
# calculate_EU2(state,  theta_2LN_bar,  theta_2LD_bar)
#============================================================================
def calculate_EU2(state,  theta_H_bar,  theta_2LN_bar,  theta_2LD_bar):
    if (theta_2LN_bar > theta_2LD_bar):
        EU2 = -nan
    else:
        EU_H = expected_utility_H(state,  theta_H_bar)
        EU2_L = expected_utility_2L(state, theta_2LN_bar,  theta_2LD_bar)
        EU2 = 0.5*(EU_H + EU2_L)

    return EU2
#============================================================================


#============================================================================
# calculate_EU3(state,  theta_2LN_bar,  theta_2LD_bar)
#============================================================================
def calculate_EU3(state,  theta_H_bar,  theta_2LN_bar,  theta_2LD_bar):
    if (theta_2LN_bar > theta_2LD_bar):
        EU3 = -nan
    else:
        # the uninformed case is just the sum of the two subcases outlined in the paper
        EU3_u = expected_utility_3u(state,  theta_H_bar)
        # while for the informed case, we need to make a distinction between the three cases
        if (theta_H_bar < theta_2LN_bar):
            EU3_i = expected_utility_3i1(state,  theta_H_bar,  theta_2LN_bar,  theta_2LD_bar)
        else:
            if (theta_H_bar < theta_2LD_bar):
                EU3_i = expected_utility_3i2(state,  theta_H_bar)
            else:
                EU3_i = expected_utility_3i3(state,  theta_H_bar,  theta_2LN_bar,  theta_2LD_bar)
        EU3 = EU3_u + EU3_i

    return EU3
#============================================================================


#============================================================================
# calculate_EU4(state,  theta_2LN_bar,  theta_2LD_bar)
#============================================================================
def calculate_EU4(state,  theta_H_bar,   theta_2LN_bar,  theta_2LD_bar):
    if (theta_2LN_bar > theta_2LD_bar):
        EU4 = -nan
    else:
        # the uninformed case is just the sum of the two subcases outlined in the paper
        EU4_u = expected_utility_4u(state)
        # while for the informed case, we need to make a distinction between the three cases
        if (theta_H_bar < theta_2LN_bar):
            EU4_i = expected_utility_4i1(state,  theta_H_bar,  theta_2LN_bar,  theta_2LD_bar)
        else:
            if (theta_H_bar < theta_2LD_bar):
                EU4_i = expected_utility_4i2(state,  theta_H_bar)
            else:
                EU4_i = expected_utility_4i3(state,  theta_H_bar,  theta_2LN_bar,  theta_2LD_bar)
        EU4 = EU4_u + EU4_i

    return EU4
#============================================================================


#============================================================================
# calculate_EU5(state)
#============================================================================
def calculate_EU5(state,  theta_bar):
    return expected_utility_5(state,  theta_bar)
#============================================================================


#============================================================================
# calculate_EU6(state)
#============================================================================
def calculate_EU6(state,  theta_bar):
    return expected_utility_6(state,  theta_bar)
#============================================================================


#============================================================================
#
#  MAIN
#
#============================================================================
if __name__ == '__main__':
    import sys

    #
    # VARIABLES
    #
    nan = 10000000000000.0
    args = sys.argv
    state = State()

    # PARAMETERS
    beta = float(args[1])          # liquidation value								[0,1]
    R = float(args[2])             # gross return in boom							[1,infty)
    phi = float(args[3])           # IB loan interest rate							[1,R]
    lamb = float(args[4])          # share of early HH								[0,1]
    eta = float(args[5])           # size of liquidity shock						weakly positive and such that lambda_L >= 0 and lambda_H <= 0
    rho = float(args[6])           # risk aversion parameter (CRRA utility)			[1,infty)
    q_H = float(args[7])           # informativeness of regional signal in H		[0,1]
    q_L=q_H                        # informativeness of regional signal in L		[0,1]

    lambda_H=lamb+eta
    lambda_L=lamb-eta

    # ENDOGENOUS PORTFOLIO CHOICE
    d_1_max = 2.0

    step_d1 = 0.01 # 1.0 <= d_1 <= d_1_max = 1.5
    step_b = 0.01 # 0.0 <= b <= eta*d_1 ~= 0.125
    step_y = 0.01 # y_min = (lamb+eta)*d_1 - b ~= 0.7 <= 1.0

    #
    # CODE
    #
    d_1 = 0.0

    maxA_EU = -nan
    maxA_d_1 = d_1
    maxA_b = 0.0
    maxA_y = min(1.0, lambda_H*d_1 - maxA_b)

    maxCE_EU = -nan
    maxCE_d_1 = d_1
    maxCE_b = 0.0
    maxCE_y = min(1.0, lambda_H*d_1 - maxCE_b)

    max1_EU = -nan
    max1_d_1 = d_1
    max1_b = 0.0
    max1_y = min(1.0, lambda_H*d_1 - max1_b)

    max2_EU = -nan
    max2_d_1 = d_1
    max2_b = 0.0
    max2_y = min(1.0, lambda_H*d_1 - max2_b)

    max3_EU = -nan
    max3_d_1 = d_1
    max3_b = 0.0
    max3_y = min(1.0, lambda_H*d_1 - max3_b)

    max4_EU = -nan
    max4_d_1 = d_1
    max4_b = 0.0
    max4_y = min(1.0, lambda_H*d_1 - max4_b)

    max5_EU = -nan
    max5_d_1 = d_1
    max5_b = 0.0
    max5_y = min(1.0, lambda_H*d_1 - max5_b)

    max6_EU = -nan
    max6_d_1 = d_1
    max6_b = 0.0
    max6_y = min(1.0, lambda_H*d_1 - max6_b)


    while (d_1 <= d_1_max):
        b=0.0
        while (b <= eta*d_1):

            y_min = 0.0#max(min(1.0, lambda_H*d_1 - b),0.0)
            y = y_min

            while (y <= 1.0):
                #print str(d_1) + " " + str(b) + " " + str(y)

                #
                # recalculate current state
                #
                state.recalculate(d_1,y,b)

                if ((y+b-lambda_H*d_1 >= 0.0) and (y-b-lambda_L*d_1 >= 0.0) and (d_1 < min(R, min((y+(1-y)*beta+b)/(lambda_H), (y+(1-y)*beta-b)/(lambda_L)) ))):
                    #
                    # case 1
                    #
                    theta_H_bar = calculate_theta_H(state)
                    a_H = q_H*theta_H_bar
                    theta_1L_bar = calculate_theta_L(state, a_H)

                    EU1 = calculate_EU1(state,  theta_H_bar,  theta_1L_bar)

                    if (EU1 > max1_EU):
                        max1_EU = EU1
                        max1_d_1 = d_1
                        max1_y = y
                        max1_b = b
                    #print str(max1_EU) + " " + str(max1_d_1) + " " + str(max1_y) + " " + str(max1_b)


                    #
                    # case 2
                    #
                    theta_H_bar = calculate_theta_H(state)
                    theta_2LD_bar = calculate_theta_LD(state)
                    theta_2LN_bar = calculate_theta_LN(state)

                    EU2 = calculate_EU2(state,  theta_H_bar,  theta_2LN_bar,  theta_2LD_bar)

                    if (EU2 > max2_EU):
                        max2_EU = EU2
                        max2_d_1 = d_1
                        max2_b = b
                        max2_y = y
                    #print str(max2_EU) + " " + str(max2_d_1) + " " + str(max2_y) + " " + str(max2_b)


                    #
                    # case 3
                    #
                    theta_H_bar = calculate_theta_H(state)
                    theta_2LD_bar = calculate_theta_L(state, q_H)
                    theta_2LN_bar = calculate_theta_LN(state)

                    EU3 = calculate_EU3(state,  theta_H_bar,  theta_2LN_bar,  theta_2LD_bar)

                    if (EU3 > max3_EU):
                        max3_EU = EU3
                        max3_d_1 = d_1
                        max3_b = b
                        max3_y = y
                    #print str(max3_EU) + " " + str(max3_d_1) + " " + str(max3_y) + " " + str(max3_b)


                    #
                    # case 4
                    #
                    theta_H_bar = calculate_theta_H(state)
                    a_H = q_H*theta_H_bar
                    theta_2LD_bar = calculate_theta_L(state, a_H)
                    theta_2LN_bar = calculate_theta_LN(state)

                    EU4 = calculate_EU4(state,  theta_H_bar,  theta_2LN_bar,  theta_2LD_bar)

                    if (EU4 > max4_EU):
                        max4_EU = EU4
                        max4_d_1 = d_1
                        max4_b = b
                        max4_y = y
                    #print str(max4_EU) + " " + str(max4_d_1) + " " + str(max4_y) + " " + str(max4_b)

                if (y-lamb*d_1 >= 0.0):
                    #
                    # case 5
                    #
                    theta_bar = calculate_theta(state)
                    EU5 = calculate_EU5(state,  theta_bar)

                    if (EU5 > max5_EU):
                        max5_EU = EU5
                        max5_d_1 = d_1
                        max5_b = b
                        max5_y = y
                    #print str(max5_EU) + " " + str(max5_d_1) + " " + str(max5_y) + " " + str(max5_b)


                    #
                    # case 6
                    #
                    theta_bar = calculate_theta(state)
                    EU6 = calculate_EU6(state,  theta_bar)

                    if (EU6 > max6_EU):
                        max6_EU = EU6
                        max6_d_1 = d_1
                        max6_b = b
                        max6_y = y
                    #print str(max6_EU) + " " + str(max6_d_1) + " " + str(max6_y) + " " + str(max6_b)

                    #
                    # autarky
                    #
                    theta_A = calculate_theta_A(state)
                    EUA = calculate_EUA(state,  theta_A)
                    if (EUA > maxA_EU):
                        maxA_EU = EUA
                        maxA_d_1 = d_1
                        maxA_y = y
                        maxA_b = b

                    #
                    # competitive equilibrium
                    #
                    theta_CE = calculate_theta_CE(state)
                    EUCE = calculate_EUCE(state,  theta_CE,  False)
                    if (EUCE > maxCE_EU):
                        maxCE_EU = calculate_EUCE(state,  theta_CE,  False)
                        maxCE_d_1 = d_1
                        maxCE_y = y
                        maxCE_b = b

                # finally, increase y
                y += step_y

            # increase b
            b += step_b

        # increase d1
        d_1 += step_d1
    # end of loop


    #
    # CALCULATE SR FOR AUTARKY
    #
    state.recalculate(maxA_d_1, maxA_y, maxA_b)
    theta_A_bar = calculate_theta_A(state)
    A_A = theta_A_bar*theta_A_bar

    #
    # CALCULATE SR FOR COMPETITIVE EQUILIBRIUM
    #
    state.recalculate(1.0, maxA_y, maxA_b)
    theta_CE_bar_A = calculate_theta_CE(state)
    A_CE_A = theta_CE_bar_A*theta_CE_bar_A

    state.recalculate(maxCE_d_1, maxCE_y, maxCE_b)
    theta_CE_bar = calculate_theta_CE(state)
    A_CE = theta_CE_bar*theta_CE_bar

    theta_H_bar_CE = calculate_theta_H(state)
    a_H_CE = q_H*theta_H_bar_CE
    theta_1L_bar_CE = calculate_theta_L(state, a_H_CE)
    A_1_CE = q_L*theta_1L_bar_CE*a_H_CE

    theta_H_bar_CE = calculate_theta_H(state)
    theta_2LN_bar_CE = calculate_theta_LN(state)
    theta_2LD_bar_CE = calculate_theta_LD(state)
    A_2_CE = q_H*q_L*theta_H_bar_CE*theta_2LD_bar_CE

    theta_bar_CE = calculate_theta(state)
    A_5_CE = q_H*q_L*theta_bar_CE
    A_6_CE = q_H*q_L*theta_bar_CE

    #
    # CALCULATE ALL POSSIBLE CONTRACTS
    #
    # for case 1
    state.recalculate(max1_d_1, max1_y, max1_b)
    theta_H_bar_1 = calculate_theta_H(state)
    a_H_1 = q_H*theta_H_bar_1
    theta_1L_bar_1 = calculate_theta_L(state, a_H_1)
    theta_2LN_bar_1 = calculate_theta_LN(state)
    theta_2LD_bar_1 = calculate_theta_LD(state)
    theta_3LN_bar_1 = calculate_theta_L(state, 0.0)
    theta_3LD_bar_1 = calculate_theta_L(state, q_H)
    theta_bar_1 = calculate_theta(state)
    # for case 2
    state.recalculate(max2_d_1, max2_y, max2_b)
    theta_H_bar_2 = calculate_theta_H(state)
    a_H_2 = q_H*theta_H_bar_2
    theta_1L_bar_2 = calculate_theta_L(state, a_H_2)
    theta_2LN_bar_2 = calculate_theta_LN(state)
    theta_2LD_bar_2 = calculate_theta_LD(state)
    theta_3LN_bar_2 = calculate_theta_L(state, 0.0)
    theta_3LD_bar_2 = calculate_theta_L(state, q_H)
    theta_bar_2 = calculate_theta(state)
    # for case 3
    state.recalculate(max3_d_1, max3_y, max3_b)
    theta_H_bar_3 = calculate_theta_H(state)
    a_H_3 = q_H*theta_H_bar_3
    theta_1L_bar_3 = calculate_theta_L(state, a_H_3)
    theta_2LN_bar_3 = calculate_theta_LN(state)
    theta_2LD_bar_3 = calculate_theta_LD(state)
    theta_3LN_bar_3 = calculate_theta_L(state, 0.0)
    theta_3LD_bar_3 = calculate_theta_L(state, q_H)
    theta_bar_3 = calculate_theta(state)
    # for case 4
    state.recalculate(max4_d_1, max4_y, max4_b)
    theta_H_bar_4 = calculate_theta_H(state)
    a_H_4 = q_H*theta_H_bar_4
    theta_1L_bar_4 = calculate_theta_L(state, a_H_4)
    theta_2LN_bar_4 = calculate_theta_LN(state)
    theta_2LD_bar_4 = calculate_theta_LD(state)
    theta_3LN_bar_4 = calculate_theta_L(state, 0.0)
    theta_3LD_bar_4 = calculate_theta_L(state, q_H)
    theta_bar_4 = calculate_theta(state)
    # for case 5
    state.recalculate(max5_d_1, max5_y, max5_b)
    theta_H_bar_5 = calculate_theta_H(state)
    a_H_5 = q_H*theta_H_bar_5
    theta_1L_bar_5 = calculate_theta_L(state, a_H_5)
    theta_2LN_bar_5 = calculate_theta_LN(state)
    theta_2LD_bar_5 = calculate_theta_LD(state)
    theta_3LN_bar_5 = calculate_theta_L(state, 0.0)
    theta_3LD_bar_5 = calculate_theta_L(state, q_H)
    theta_bar_5 = calculate_theta(state)
    # for case 6
    state.recalculate(max6_d_1, max6_y, max6_b)
    theta_H_bar_6 = calculate_theta_H(state)
    a_H_6 = q_H*theta_H_bar_6
    theta_1L_bar_6 = calculate_theta_L(state, a_H_6)
    theta_2LN_bar_6 = calculate_theta_LN(state)
    theta_2LD_bar_6 = calculate_theta_LD(state)
    theta_3LN_bar_6 = calculate_theta_L(state, 0.0)
    theta_3LD_bar_6 = calculate_theta_L(state, q_H)
    theta_bar_6 = calculate_theta(state)


    #
    # CALCULATE SR FOR CASE (1)
    #
    A_1 = q_L*theta_1L_bar_1*a_H_1
    A_1_2 = q_L*theta_1L_bar_2*a_H_2
    A_1_3 = q_L*theta_1L_bar_3*a_H_3
    A_1_4 = q_L*theta_1L_bar_4*a_H_4
    A_1_5 = q_L*theta_1L_bar_5*a_H_5
    A_1_6 = q_L*theta_1L_bar_6*a_H_6

    #
    # CALCULATE SR FOR CASE (2)
    #
    A_2 = q_H*q_L*theta_H_bar_2*theta_2LD_bar_2
    A_2_1 = q_H*q_L*theta_H_bar_1*theta_2LD_bar_1
    A_2_3 = q_H*q_L*theta_H_bar_3*theta_2LD_bar_3
    A_2_4 = q_H*q_L*theta_H_bar_4*theta_2LD_bar_4
    A_2_5 = q_H*q_L*theta_H_bar_5*theta_2LD_bar_5
    A_2_6 = q_H*q_L*theta_H_bar_6*theta_2LD_bar_6

    #
    # CALCULATE SR FOR CASE (3)
    #
    A_3 = q_H*q_L*min(theta_H_bar_3, theta_3LD_bar_3)
    A_3_1 = q_H*q_L*min(theta_H_bar_1 , theta_3LD_bar_1)
    A_3_2 = q_H*q_L*min(theta_H_bar_2 , theta_3LD_bar_2)
    A_3_4 = q_H*q_L*min(theta_H_bar_4 , theta_3LD_bar_4)
    A_3_5 = q_H*q_L*min(theta_H_bar_5, theta_3LD_bar_5)
    A_3_6 = q_H*q_L*min(theta_H_bar_6 , theta_3LD_bar_6)

    #
    # CALCULATE SR FOR CASE (4)
    #
    A_4 = (q_H + (1.0-q_H)*q_L)*min(theta_H_bar_4,theta_2LD_bar_4)
    A_4_1 = (q_H + (1.0-q_H)*q_L)*min(theta_H_bar_1,theta_2LD_bar_1)
    A_4_2 = (q_H + (1.0-q_H)*q_L)*min(theta_H_bar_2,theta_2LD_bar_2)
    A_4_3 = (q_H + (1.0-q_H)*q_L)*min(theta_H_bar_3,theta_2LD_bar_3)
    A_4_5 = (q_H + (1.0-q_H)*q_L)*theta_H_bar_5
    A_4_6 = (q_H + (1.0-q_H)*q_L)*theta_H_bar_6

    #
    # CALCULATE SR FOR CASE (5)
    #
    A_5 = q_H*q_L*theta_bar_5
    A_5_1 = q_H*q_L*theta_bar_1
    A_5_2 = q_H*q_L*theta_bar_2
    A_5_3 = q_H*q_L*theta_bar_3
    A_5_4 = q_H*q_L*theta_bar_4
    A_5_6 = q_H*q_L*theta_bar_6

    #
    # CALCULATE SR FOR CASE (6)
    #
    A_6 = q_H*q_L*theta_bar_6
    A_6_1 = q_H*q_L*theta_bar_1
    A_6_2 = q_H*q_L*theta_bar_2
    A_6_3 = q_H*q_L*theta_bar_3
    A_6_4 = q_H*q_L*theta_bar_4
    A_6_5 = q_H*q_L*theta_bar_5


    #
    # CALCULATE SIR
    #
    SIR_low = A_4 - A_6 - A_1
    SIR_high = A_4 - A_5 - A_2
    # and for non-optimal contracts
    SIR_low_1 = A_4_1 - A_6_1 - A_1
    SIR_high_1 = A_4_1 - A_5_1 - A_2_1
    SIR_low_2 = A_4_2 - A_6_2 - A_1_2
    SIR_high_2 = A_4_2 - A_5_2 - A_2
    SIR_low_3 = A_4_3 - A_6_3 - A_1_3
    SIR_high_3 = A_4_3 - A_5_3 - A_2_3
    SIR_low_4 = A_4 - A_6_4 - A_1_4
    SIR_high_4 = A_4 - A_5_4 - A_2_4
    SIR_low_5 = A_4_5 - A_6_5 - A_1_5
    SIR_high_5 = A_4_5 - A_5 - A_2_5
    SIR_low_6 = A_4_6 - A_6 - A_1_6
    SIR_high_6 = A_4_6 - A_5_6 - A_2_6


    #
    # CALCULATE NON-OPTIMAL CONTRACTS FOR COMPARISON
    #
    state.recalculate(1.0 , maxA_y, maxA_b)
    theta_CE_bar_A = calculate_theta_CE(state)
    EUCE_A = calculate_EUCE(state,  theta_CE_bar_A,  False)

    state.recalculate(maxCE_d_1, maxCE_y, maxCE_b)
    theta_CE = calculate_theta_CE(state)
    theta_H_bar = calculate_theta_H(state)
    a_H = q_H*theta_H_bar
    theta_1L_bar = calculate_theta_L(state, a_H)
    theta_2LN_bar = calculate_theta_LN(state)
    theta_2LD_bar = calculate_theta_LD(state)
    theta_bar = calculate_theta(state)
    EU1_CE = calculate_EU1(state,  theta_H_bar,  theta_1L_bar)
    EU2_CE = calculate_EU2(state,  theta_H_bar,  theta_2LN_bar,  theta_2LD_bar)
    EU5_CE = calculate_EU5(state,  theta_bar)
    EU6_CE = calculate_EU6(state,  theta_bar)

    state.recalculate(max1_d_1, max1_y, max1_b)
    theta_H_bar = calculate_theta_H(state)
    theta_2LN_bar = calculate_theta_LN(state)
    theta_2LD_bar = calculate_theta_LD(state)
    EU2_1 = calculate_EU2(state,  theta_H_bar,  theta_2LN_bar,  theta_2LD_bar)
    EU3_1 = calculate_EU3(state,  theta_H_bar,  theta_2LN_bar,  theta_2LD_bar)
    EU4_1 = calculate_EU4(state,  theta_H_bar,  theta_2LN_bar,  theta_2LD_bar)

    state.recalculate(max5_d_1,  max5_y,  max5_b)
    theta_H_bar = calculate_theta_H(state)
    theta_2LN_bar = calculate_theta_LN(state)
    theta_2LD_bar = calculate_theta_LD(state)
    theta_bar = calculate_theta(state)
    EU3_5 = calculate_EU3(state,  theta_H_bar,  theta_2LN_bar,  theta_2LD_bar)
    EU4_5 = calculate_EU4(state,  theta_H_bar,  theta_2LN_bar,  theta_2LD_bar)
    EU6_5 = calculate_EU6(state,  theta_bar)

    state.recalculate(max2_d_1,  max2_y,  max2_b)
    theta_H_bar = calculate_theta_H(state)
    theta_2LN_bar = calculate_theta_LN(state)
    theta_2LD_bar = calculate_theta_LD(state)
    EU4_2 = calculate_EU4(state,  theta_H_bar,  theta_2LN_bar,  theta_2LD_bar)

    state.recalculate(max3_d_1,  max3_y,  max3_b)
    theta_H_bar = calculate_theta_H(state)
    theta_2LN_bar = calculate_theta_LN(state)
    theta_2LD_bar = calculate_theta_LD(state)
    EU4_3 = calculate_EU4(state,  theta_H_bar,  theta_2LN_bar,  theta_2LD_bar)

    state.recalculate(max6_d_1,  max6_y,  max6_b)
    theta_H_bar = calculate_theta_H(state)
    theta_2LN_bar = calculate_theta_LN(state)
    theta_2LD_bar = calculate_theta_LD(state)
    EU4_6 = calculate_EU4(state,  theta_H_bar,  theta_2LN_bar,  theta_2LD_bar)


    #
    # print the latex table with the results
    #
    fileName = "results-" + str(beta) + "-" + str(R) + "-" + str(phi) + "-" + str(lamb) + "-" + str(eta) + "-" + str(rho) + "-" + str(q_H) + ".tex"
    latexOutput = open(fileName,  'w')
    #
    # create the header
    #
    text = "\\begin{table}[h]\n"
    text += "\centering \n"
    text += "{\small"
    text += "\\begin{tabular}{lcccc} \n" # 5 cols
    text += "  \\toprule \n"
    text += "  & cr & cr + ic & ce & ce + ic \\\\ \n"
    text += "  & ($EU$, $d_1^*$, $y^*$, $b^*$) & ($EU$, $d_1^*$, $y^*$, $b^*$) & ($EU$, $d_1^*$, $y^*$, $b^*$) & ($EU$, $d_1^*$, $y^*$, $b^*$) \\\\ \n"
    text += "  & ($\\thetaH$, $\\thetaiL$ , $A_{\\textrm{cr}}$) & ($\\thetaH$, $\\thetaiiLN$ , $\\thetaiiLD$, $A_{\\textrm{cr+ic}}$) & ($\\oline{\\theta}$, $A_{\\textrm{ce}}$) & ($\\oline{\\theta}$, $A_{\\textrm{ce+ic}}$) \\\\ \n"
    text += "  \midrule \n"

    #
    # now the results
    #
    # cr
    text += " cr & (" + str(round(max1_EU, 3))  + "," + str(round(max1_d_1, 3))  + "," + str(round(max1_y, 3)) + "," + str(round(max1_b, 3)) + ") & (" + str(round(EU2_1, 3))  + "," + str(round(max1_d_1, 3))  + "," + str(round(max1_y, 3)) + "," + str(round(max1_b, 3)) + ") & & \\\\ \n"
    text += " & (" + str(round(theta_H_bar_1, 3))  + "," + str(round(theta_1L_bar_1, 3)) + "," + str(round(A_1, 3)) + ") & (" + str(round(theta_H_bar_1, 3))  + "," + str(round(theta_2LN_bar_1, 3)) + "," + str(round(theta_2LD_bar_1, 3)) + ","+ str(round(A_2_1, 3)) + ")  & & \\vspace{0.3cm} \\\\ \n"
    #	text += " & & & & \\\\ \n"
    # ib + info
    text += "cr + & & (" + str(round(max2_EU, 3))  + "," + str(round(max2_d_1, 3))  + "," + str(round(max2_y, 3)) + "," + str(round(max2_b, 3)) + ") & & \\\\ \n"
    text += "ic   & & (" + str(round(theta_H_bar_2, 3))  + "," + str(round(theta_2LN_bar_2, 3)) + "," + str(round(theta_2LD_bar_2, 3)) + ","+ str(round(A_2, 3)) + ") & & \\vspace{0.3cm} \\\\ \n"
    #	text += " & & & & \\\\ \n"
    # pure cs
    text += " ce & & & (" + str(round(max5_EU, 3))  + ","+ str(round(max5_d_1, 3))  + "," + str(round(max5_y, 3)) + "," + str(round(max5_b, 3)) + ") & (" + str(round(EU6_5, 3))  + "," + str(round(max5_d_1, 3))  + "," + str(round(max5_y, 3)) + "," + str(round(max5_b, 3)) + ") \\\\ \n"
    text += " & & & (" + str(round(theta_bar_5, 3))  + ","+ str(round(A_5, 3)) + ") & (" + str(round(theta_bar_5, 3))  + ","+ str(round(A_6_5, 3)) + ") \\vspace{0.3cm} \\\\ \n"
    #	text += " & & & & \\\\ \n"
    # cs+info
    text += " ce + & & & & (" + str(round(max6_EU, 3))  + ","+ str(round(max6_d_1, 3))  + "," + str(round(max6_y, 3)) + "," + str(round(max6_b, 3)) + ") \\\\ \n"
    text += " ic   & & & & (" + str(round(theta_bar_6, 3))  + ","+ str(round(A_6, 3)) + ") \\\\ \n"
    text += "\\bottomrule \n"
    #
    # and the footer
    #
    text += "\end{tabular} }\n"
    text += "\caption{Equilibrium allocation for different forms of financial fragility for calibration $\\beta$=" + str(beta) + ", $R$=" + str(R) + ", $\\phi$=" + str(phi) + ", $\\lambda$=" + str(lamb) + ", $\\eta$=" + str(eta)  + ", $\\rho$=" + str(rho) + ", $q_H$=" + str(q_H) + ". Expected utility $(EU)$, portfolio choice variables $(d_1,y,b)$, withdrawal thresholds $(\\oline{\\theta}_H, \\oline{\\theta}_{1,L}, \\oline{\\theta}^N_{2,L}, \\oline{\\theta}^D_{2,L}, \\oline{\\theta})$, and systemic financial fragility $(A_{\\textrm{cr}}, A_{\\textrm{cr+ic}}, A_{\\textrm{ce}}, A_{\\textrm{ce+ic}})$ in the different model variants (cr: counterparty risk, ic: information contagion, ce: common exposure).} \n"
    text += "\label{Table::Results:" + str(beta) + "-" + str(R) + "-" + str(phi) + "-" + str(lamb) + "-" + str(eta) + "-" + str(rho) + "-" + str(q_H)  + "} \n"
    text += "\end{table} \n"
    # and write the text
    latexOutput.write(text)
    latexOutput.close()


    #
    # and also for the discussion results, cs+ib vs unified
    #
    fileName = "discussion-" + str(beta) + "-" + str(R) + "-" + str(phi) + "-" + str(lamb) + "-" + str(eta) + "-" + str(rho) + "-" + str(q_H) + ".tex"
    latexOutput = open(fileName,  'w')
    #
    # create the header
    #
    text = "\\begin{table}[h] \n"
    text += "\centering \n"
    text += "{\small"
    text += "\\begin{tabular}{ccc} \n" # 7 cols
    text += "  \\toprule \n"
    text += "  & cr + ce & unified \\\\ \n"
    text += "  & ($EU$, $d_1^*$, $y^*$, $b^*$) & ($EU$, $d_1^*$, $y^*$, $b^*$) \\\\ \n"
    text += "  & ($\\thetaH$, $\\thetaiiiLN$ , $\\thetaiiiLD$, $A_{\\textrm{cr+ce}}$) & ($\\thetaH$, $\\thetaiiLN$ , $\\thetaiiLD$, $A_{\\textrm{unified}}$) \\\\ \n"
    text += "  \\midrule \n"

    #
    # now the results
    #
    # ib + cs
    text += " cr + & (" + str(round(max3_EU, 3))  + "," + str(round(max3_d_1, 3))  + "," + str(round(max3_y, 3)) + "," + str(round(max3_b, 3)) + ") & (" + str(round(EU4_3, 3))  + "," + str(round(max3_d_1, 3))  + "," + str(round(max3_y, 3)) + "," + str(round(max3_b, 3)) + ") \\\\ \n"
    text += " ce  & (" + str(round(theta_H_bar_3, 3))  + "," + str(round(theta_3LN_bar_3, 3)) + "," + str(round(theta_3LD_bar_3, 3)) + ","+ str(round(A_3, 3)) + ") & (" + str(round(theta_H_bar_3, 3))  + "," + str(round(theta_2LN_bar_3, 3)) + "," + str(round(theta_2LD_bar_3, 3)) + ","+ str(round(A_4_3, 3)) + ") \\vspace{0.3cm} \\\\ \n"

    # unified
    text += " unified & & (" + str(round(max4_EU, 3))  + ","+ str(round(max4_d_1, 3))  + "," + str(round(max4_y, 3)) + "," + str(round(max4_b, 3)) + ") \\\\ \n"
    text += " & & (" + str(round(theta_H_bar_4, 3))  + "," + str(round(theta_2LN_bar_4, 3)) + "," + str(round(theta_2LD_bar_4, 3)) + ","+ str(round(A_4, 3)) + ") \\\\ \n"

    #
    # and the footer
    #
    text += "  \\bottomrule \n"
    text += "\end{tabular} }\n"
    text += "\caption{Equilibrium allocation for different forms of financial fragility for calibration $\\beta$=" + str(beta) + ", $R$=" + str(R) + ", $\\phi$=" + str(phi) + ", $\\lambda$=" + str(lamb) + ", $\\eta$=" + str(eta)  + ", $\\rho$=" + str(rho) + ", $q_H$=" + str(q_H) + ". Expected utility $(EU)$, portfolio choice variables $(d_1,y,b)$, withdrawal thresholds $(\\oline{\\theta}_H, \\oline{\\theta}^N_{3,L}, \\oline{\\theta}^D_{3,L})$, and systemic financial fragility $(A_{\\textrm{cr+ce}}, A_{\\textrm{unified}})$ in different model variants (cr: counterparty risk, ce: common exposure, unified: unified model of contagion).} \n"
    text += "\label{Table::Discussion:" + str(beta) + "-" + str(R) + "-" + str(phi) + "-" + str(lamb) + "-" + str(eta) + "-" + str(rho) + "-" + str(q_H)  + "} \n"
    text += "\end{table} \n"
    # and write the text
    latexOutput.write(text)
    latexOutput.close()


    #
    # print the comparison of sir
    #
    fileName = "sir-" + str(beta) + "-" + str(R) + "-" + str(phi) + "-" + str(lamb) + "-" + str(eta) + "-" + str(rho) + "-" + str(q_H) + ".tex"
    latexOutput = open(fileName,  'w')
    #
    # create the header
    #
    text = "\\begin{table}[h] \n"
    text += "\centering \n"
    text += "{\small"
    text += "\\begin{tabular}{ccc} \n"
    text += "  \\toprule \n"
    text += "  portfolio & $\\overline{SIR}$ & $\\underline{SIR}$ \\\\ \n"
    text += "  choice & &  \\\\ \n"
    text += "  \\midrule \n"

    #
    # now the results
    #
    text += " optimal & " + str(round(SIR_high, 3))  + " & " + str(round(SIR_low, 3)) + "\\\\ \n"
    text += " cr & " + str(round(SIR_high_1, 3))  + " & " + str(round(SIR_low_1, 3)) + "\\\\ \n"
    text += " cr+ic & " + str(round(SIR_high_2, 3))  + " & " + str(round(SIR_low_2, 3)) + "\\\\ \n"
    text += " ce & " + str(round(SIR_high_3, 3))  + " & " + str(round(SIR_low_3, 3)) + "\\\\ \n"
    text += " ce+ic & " + str(round(SIR_high_4, 3))  + " & " + str(round(SIR_low_4, 3)) + "\\\\ \n"
    text += " cr+ce & " + str(round(SIR_high_5, 3))  + " & " + str(round(SIR_low_5, 3)) + "\\\\ \n"
    text += " unified & " + str(round(SIR_high_6, 3))  + " & " + str(round(SIR_low_6, 3)) + "\\\\ \n"

    #
    # and the footer
    #
    text += "  \\bottomrule \n"
    text += "\end{tabular} }\n"
    text += "\caption{Systemic interaction risk for different portfolio allocations for calibration $\\beta$=" + str(beta) + ", $R$=" + str(R) + ", $\\phi$=" + str(phi) + ", $\\lambda$=" + str(lamb) + ", $\\eta$=" + str(eta)  + ", $\\rho$=" + str(rho) + ", $q_H$=" + str(q_H) + ". Upper bound $(\\overline{\\textrm{SIR}})$ and lower bound $(\\underline{\\textrm{SIR}})$ on systemic interaction risk evaluated at different portfolio choices. Optimal: all contributions are evaluated at their respective optimal portfolio choices. In all other cases, the portfolio choice of a given model is being kept constant to evaluate all contributions to systemic interaction risk (cr: counterparty risk; ic: information contagion; ce: common exposure; unified: unified model of contagion).} \n"
    text += "\label{Table::SIR:" + str(beta) + "-" + str(R) + "-" + str(phi) + "-" + str(lamb) + "-" + str(eta) + "-" + str(rho) + "-" + str(q_H)  + "} \n"
    text += "\end{table} \n"
    # and write the text
    latexOutput.write(text)
    latexOutput.close()


    #
    # and print out the raw data we need e.g. for check_extreme_values.py
    #
    # Format:
    # Parameters (7) EU d_1 y b (12,17,22,27, 32, 37) theta_H (42)
    print str(beta) + " " + str(R) + " " + str(phi) + " " + str(lamb) + " " + str(eta) + " " + str(rho) + " " + str(q_L) + " XXX " \
          + str(round(max1_EU,5)) + " " + str(round(max1_d_1,5)) + " " + str(round(max1_y,5)) + " " + str(round(max1_b,5)) + " X " \
          + str(round(max2_EU,5)) + " " + str(round(max2_d_1,5)) + " " + str(round(max2_y,5)) + " " + str(round(max2_b,5)) + " X " \
          + str(round(max3_EU,5)) + " " + str(round(max3_d_1,5)) + " " + str(round(max3_y,5)) + " " + str(round(max3_b,5)) + " X " \
          + str(round(max4_EU,5)) + " " + str(round(max4_d_1,5)) + " " + str(round(max4_y,5)) + " " + str(round(max4_b,5)) + " X " \
          + str(round(max5_EU,5)) + " " + str(round(max5_d_1,5)) + " " + str(round(max5_y,5)) + " " + str(round(max5_b,5)) + " X " \
          + str(round(max6_EU,5)) + " " + str(round(max6_d_1,5)) + " " + str(round(max6_y,5)) + " " + str(round(max6_b,5)) + " XXX " \
          + str(round(theta_H_bar_1,5)) + " " + str(round(theta_H_bar_2,5)) + " " + str(round(theta_H_bar_3,5)) + " " + str(round(theta_H_bar_4,5)) + " X " \
          + str(round(theta_1L_bar_1,5)) + " " + str(round(theta_2LN_bar_2,5)) + " " + str(round(theta_2LD_bar_2,5)) + " " + str(round(theta_3LN_bar_3,5)) + " " + str(round(theta_3LD_bar_3,5)) + " " + str(round(theta_2LD_bar_4,5)) + str(round(theta_bar,5)) + " XXX " \
          + str(round(A_1,5)) + " " + str(round(A_2,5)) + " " + str(round(A_3,5)) + " " + str(round(A_4,5)) + " " + str(round(A_5,5)) + " " + str(round(A_6,5)) + " XXX " \
          + str(round(maxA_EU, 5)) + " " + str(round(maxA_d_1, 5)) + " " + str(round(maxA_y, 5)) + " " + str(round(maxA_b, 5)) + " X " \
          + str(round(maxCE_EU, 5)) + " " + str(round(maxCE_d_1, 5)) + " " + str(round(maxCE_y, 5)) + " " + str(round(maxCE_b, 5))  + " X " \
          + str(round(theta_A_bar, 5)) + " " + str(round(theta_CE_bar, 5)) + " X " + str(round(A_A, 5)) + " " + str(round(A_CE, 5))
