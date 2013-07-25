# -!- coding=utf8 -!-
from __future__ import division

import networkx as nx

def make_graph(pmi, gpickle_path = "data/douguo.gpickle"):
    """(dict) => Graph"""
    #init graph
    g = nx.Graph()

    #get list of (ig1, ig2, pcm value, the weight)
    pair_with_weights = map(lambda key: (key[0], key[1], pmi[key]), pmi.keys())
    
    #add the pairs to the graph
    g.add_weighted_edges_from(pair_with_weights)

    #nx.write_gml(g, gpickle_path)
    #print "to gml"
    
    nx.write_gpickle(g, gpickle_path)
    
    return g

def add_category_for_ingredients(gpickle_path = "data/douguo.gpickle"):
    """add category for ingredients, then save it to gpickle"""
    from util import load_ingredient_category_mapping
    
    g = nx.read_gpickle(gpickle_path)
    m = load_ingredient_category_mapping()

    for name in g.node:
        g.node[name]["category"] = m[name]

    nx.write_gpickle(g, gpickle_path)
    
    return g

        
def main():
    """
    from cPickle import load
    pmi = load(open("data/pmi.pickle"))
    make_graph(pmi)
    """

    add_category_for_ingredients()
    
if __name__ == "__main__":
    main()
