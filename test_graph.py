# -!- encoding=utf8 -!-

from __future__ import division
import unittest 
import numpy as np

from graph import make_graph
from prob import IngProbTable

import networkx as nx

potato = "土豆".decode("utf8")
beef = "牛肉".decode("utf8")
pepper = "辣椒".decode("utf8")
tomato = "番茄".decode("utf8")
egg = "鸡蛋".decode("utf8")
hair = "头发".decode("utf8")
ing_list = [[potato, beef, pepper], [tomato, beef], [tomato, egg], [potato, pepper]]
table = IngProbTable(ing_list)
        

class MakeGraphTestCase(unittest.TestCase):
    def setUp(self):
        self.g = make_graph(table)
        nx.write_gml(self.g, "data/simply_graph.gml")

    def test_node_count(self):
        """whether node count matches 5"""
        expected = 5
        actual = self.g.number_of_nodes()

        self.assertEqual(expected, actual)
        
    def test_edge_count(self):
        """whether edge count matches 5"""
        expected = 5
        actual = self.g.number_of_edges()

        self.assertEqual(expected, actual)
        
        import matplotlib as mpl

        print mpl.rcParams["font.serif"]
        nx.draw(self.g)
        from matplotlib import pyplot as plt
        plt.show()
        

if __name__ == "__main__":
    unittest.main()

