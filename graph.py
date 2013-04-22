# -!- coding=utf8 -!-
from __future__ import division

import networkx as nx

from source import load_ing_prob_table_from_pickle


def make_graph(tbl):
    """(IngProbTable) => Graph"""
    #init graph
    g = nx.Graph()

    #get list of (ig1, ig2, pcm value, the weight)
    pair_with_weights = map(lambda pair: (pair[0], pair[1], tbl[pair]), tbl.pairs)
    
    #add the pairs to the graph
    g.add_weighted_edges_from(pair_with_weights)

    return g

def prob_tbl_pickle_to_gml(tbl_path="data/douguo.pickle", gml_path="data/douguo.gml"):
    tbl = load_ing_prob_table_from_pickle(tbl_path)
    print "finished loading pickle"

    g = make_graph(tbl)
    print "made graph"

    nx.write_gml(g, gml_path)
    print "to file"
    
    nx.write_gpickle(g, gml_path.split('.')[0] + '.gpickle')
    print "to gpickle"

def main():
    
    prob_tbl_pickle_to_gml("data/douguo.pickle", "data/test/douguo.gml")
    
    """
    import jieba

    g = nx.read_gpickle("data/test/douguo.gpickle")
    for n in g.nodes():
        print "/ ".join(jieba.cut(n.encode("utf8"), cut_all=False))
    """

if __name__ == "__main__":
    main()
