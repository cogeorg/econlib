__author__ = """Co-Pierre Georg (co-pierre.georg@uct.ac.za)"""

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
        G_agg.add_node(fromID)
        G_agg.add_node(toID)
        # if link exists, update it
        for u, v, edata in G_agg.edges(data=True):
            if str(u) == fromID and str(v) == toID:
                found = True
                edata['weight'] += link_weight
        # if not, add it
        if not found:
            G_agg.add_edge(fromID, toID, weight=link_weight)
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

        Parameters
        ----------
        G_agg: A networkx.DiGraph() object
        G: The network that is to be added to the aggregate (networkx.DiGraph())

        Returns
        -------
        None

        Note
        ----
        add_link only works for weighted networks.
        """
        G_agg.add_nodes_from(G.nodes())
        for u, v, edata in G.edges(data=True):
            add_link(G_agg, str(u), str(v), edata['weight'])


    def compute_node_properties(self, G):
        """
        Parameters
        ----------
        G: A networkx.DiGraph() object

        Returns
        -------
        self.nodes: A list of Node objects where (list)
        """
        self.nodes = []

        for node in G.nodes():
            _node = Node(str(node))
            _node.out_degree = G.out_degree(node,weight='weight')
            _node.in_degree = G.in_degree(node,weight='weight')
            self.nodes.append(_node)
