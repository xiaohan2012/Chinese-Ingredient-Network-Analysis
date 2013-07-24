# -!- coding=utf8 -!-
from __future__ import division

from recipe import IngredientPair
from extract import extract_items, extract_pairs


import numpy as np


def make_prob_table(pair_list, item_list, recipe_count):
    """
    make the ingredient pair and item probability tables
    """
    from collections import Counter
    pair_freq = Counter(pair_list)
    item_freq = Counter(item_list)
    
    #ingredient pair prob table
    pair_prob = dict(((pair, freq / recipe_count) for pair, freq in pair_freq.items()))

    #ingredient item prob table
    item_prob = dict(((item, freq / recipe_count) for item, freq in item_freq.items()))

    return pair_prob, item_prob

class IngProbTable(object):
    """ the probability table for ingredient pair and ingredient item"""
    
    def __init__(self, ing_list):
        """ 
        (list of list of str) => IngProbTable
        
        given the ingredients list
        """
        #load pairs and items
        self.pairs = extract_pairs(ing_list)
        self.items = extract_items(ing_list)
        
        #recipe_count
        self.recipe_count = len(ing_list)
        
        #make probability table
        self.pair_prob, self.item_prob = make_prob_table(self.pairs, self.items, self.recipe_count)
        
        
    def __getitem__(self, key):
        """
        (tuple of(Ingredient, Ingredient) or Ingredient) => float
        
        return the prob of the ingredient pair or the single ingredient item
        """
        if isinstance(key, tuple):
            return self.pair_prob.get((IngredientPair(*key)), 0)
        elif isinstance(key, unicode):
            return self.item_prob.get(key, 0)
        else:
            raise KeyError("Invalid Key %s" %key.encode("utf8"))

    def pmi(self, ing1, ing2):
        """(Ingredient, Ingredient) => float
        return the PMI value of ingredient 1 and ingredient 2.
        PMI = log(p(a, b)/(p(a)p(b)))
        """
        numer = self[IngredientPair(ing1, ing2)]
        denom = self[ing1] * self[ing2]
        if numer == 0 or denom == 0:
            return float("-inf")
        else:
            return np.log( numer / denom)

def pickle_ing_prob_table(path):
    """
    (str) => None
    
    given the recipe path, pickle the ingredient probability table
    """
    from source import load_ing_prob_table_from_file

    tbl = load_ing_prob_table_from_file(path)
    print "made table"

    from cPickle import dump
    dump(tbl, open(path + ".pickle", "w"))
    print "to file"

def main():
    pickle_ing_prob_table("data/test/douguo.recipe")

def test():
    import doctest
    doctest.testmod()
    #doctest.run_docstring_examples(load_ing_gprob_table_from_pickle, globals())
    
if __name__ == "__main__":
    test()
#    main()
