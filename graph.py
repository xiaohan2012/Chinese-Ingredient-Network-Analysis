# -!- coding=utf8 -!-
from __future__ import division

import networkx as nx

def make_graph(pmi, gml_path = "data/douguo.gml"):
    """(dict) => Graph"""
    #init graph
    g = nx.Graph()

    #get list of (ig1, ig2, pcm value, the weight)
    pair_with_weights = map(lambda key: (key[0], key[1], pmi[key]), pmi.keys())
    
    #add the pairs to the graph
    g.add_weighted_edges_from(pair_with_weights)

    nx.write_gml(g, gml_path)
    print "to gml"
    
    #nx.write_gpickle(g, gml_path.split('.')[0] + '.gpickle')
    #print "to gpickle"
    
    return g

def main():
    from cPickle import load
    pmi = load(open("data/pmi.pickle"))
    make_graph(pmi)

if __name__ == "__main__":
    main()
