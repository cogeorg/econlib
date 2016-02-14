#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = """Co-Pierre Georg (co-pierre.georg@uct.ac.za)"""

import sys
import networkx as nx
from src.networktools import Network


#-------------------------------------------------------------------------
#
#  networks.py is a collection of helpers for networkx
#
#-------------------------------------------------------------------------
if __name__ == '__main__':

#
# VARIABLES
#
    args = sys.argv


    test_number = args[1]

    #
    # TEST 1: compute_node_properties
    #
    if test_number == "1":
        network = Network()

        # read test network
        network_file_name = args[2]
        G = nx.read_gexf(network_file_name)

        # test network
        network.compute_node_properties(G)

        for node in network.nodes:
            print node.identifier, node.out_degree, node.in_degree
