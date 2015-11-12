#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = """Co-Pierre Georg (co-pierre.georg@uct.ac.za)"""

import sys
import logging
import re

import networkx as nx

from math import sqrt

from src.node import Node



#-------------------------------------------------------------------------
#
#  class Network
#
#-------------------------------------------------------------------------
class Network(object):
    __version__ = 0.9

#
# VARIABLES
#
    nodes = []

#
# METHODS -- HELPER METHODS
#
    #-------------------------------------------------------------------------
    #  __init__
    #-------------------------------------------------------------------------
    def __init__(self):
        pass
    #-------------------------------------------------------------------------

    #-------------------------------------------------------------------------
    # add_link(G_agg, fromID, toID, weight)
    #-------------------------------------------------------------------------
    def add_link(G_agg,  fromID,  toID,  link_weight):
        found = False
        # add nodes first
        G_agg.add_node(fromID) # add_node checks if nodes exist already and doesn't add them twice
        G_agg.add_node(toID)
        # if link exists, update it
        for u, v, edata in G_agg.edges(data=True):
            if str(u) == fromID and str(v) == toID:
                found = True
                edata['weight'] += link_weight
        # if not, add it
        if not found:
            G_agg.add_edge(fromID,  toID,  weight=link_weight)
    #-------------------------------------------------------------------------


#
# METHODS -- WORKER METHODS
#
    #-------------------------------------------------------------------------
    #
    #-------------------------------------------------------------------------
    def add_networks(self, G_agg, G):
        """
        Adds the second network to the first

        Args:
            G_agg (networkx.DiGraph()) -- The aggregate network
            G (networkx.DiGraph()) -- The network that is to be added to the aggregate

        Returns:
            None

        Note:
        - add_link only works for weighted networks.
        """
        G_agg.add_nodes_from(G.nodes())
        for u, v, edata in G.edges(data=True):
            add_link(G_agg, str(u), str(v), edata['weight'])
    #-------------------------------------------------------------------------


    #-------------------------------------------------------------------------
    #
    #-------------------------------------------------------------------------
    def compute_node_properties(self, network):
        """
        Args:
            network (networkx.DiGraph()) -- A weighted, directed networkx DiGraph

        Returns:
            self.nodes (list) -- A list of Node objects where

        """
        self.nodes = []

        for node in network.nodes():
            _node = Node(str(node))
            _node.out_degree = network.out_degree(node, weight='weight')
            _node.in_degree = network.in_degree(node, weight='weight')
            self.nodes.append(_node)