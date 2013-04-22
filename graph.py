# -!- coding=utf8 -!-
from __future__ import division

import networkx as nx

from prob import *

def make_graph(tbl):
    """(IngProbTable) => Graph"""
    #init graph
    g = nx.Graph()

    #get list of (ig1, ig2, pcm value, the weight)
    pair_with_weights = map(lambda pair: (pair[0], pair[1], tbl[pair]), tbl.pairs)
    
    #add the pairs to the graph
    g.add_weighted_edges_from(pair_with_weights)

    return g

def main():
    tbl = load_ing_prob_table_from_pickle("data/douguo.recipe.pickle")
    print "finished loading pickle"

    g = make_graph(tbl)
    print "made graph"

    nx.write_gml(g, "data/douguo.gml")
    print "to file"

if __name__ == "__main__":
    main()
