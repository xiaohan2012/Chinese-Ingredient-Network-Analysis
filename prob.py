# -!- coding=utf8 -!-
from __future__ import division

from preprocess import *
import numpy as np

def load_ing_list(path="data/douguo.recipe"):
    """load the ingredient list, in forms of [[a,b],[c,d,e]]"""

    recipes = load_corrected_recipe_from_file(path)
    ing_list = extract_recipe_ingredient_list(recipes)
    return ing_list

class IngredientPair(tuple):
    """class for ingredient pair
    
    >>> potato = "土豆".decode("utf8")
    >>> tomato = "番茄".decode("utf8")
    >>> p1 = IngredientPair(potato, tomato)
    >>> p2 = IngredientPair(tomato, potato)
    >>> p1 == p2 #test for object equality
    True
    >>> len(set([p1,p2])) #p1 and p2 should be considered identical in a set
    1
    >>> print p1
    土豆 + 番茄
    >>> from collections import Counter
    >>> c = Counter([p1,p2]) #for a counter, p1 and p2 should count towards the same thing
    >>> c[p1]
    2
    """
    def __new__(cls, i1, i2):
        #because tuple is immutable, use __new__
        return tuple.__new__(cls, (i1, i2))
        
    def __eq__(self, other):
        """int terms of ingredient pair, 
        (土豆,番茄) is the same as (番茄,土豆)"""
        
        return (self[0] == other[0] and self[1] == other[1]) or (self[0] == other[1] and self[1] == other[0])
    
    def __str__(self):
        i1, i2 = sorted(list(self))
        return "%s + %s" %(i1.encode("utf8"), i2.encode("utf8"))

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(" ".join(sorted(list(self))))

def make_ing_pairs(pair_list):
    """(list of tuple) => list of IngredientPair
    >>> i1 = "土豆".decode("utf8")
    >>> i2 = "番茄".decode("utf8")
    >>> i3 = "鸡蛋".decode("utf8")
    >>> ing_list = make_ing_pairs([(i1,i2),(i2,i1),(i2,i3)])
    >>> print ing_list
    [土豆 + 番茄, 土豆 + 番茄, 番茄 + 鸡蛋]
    """
    return map(lambda pair: IngredientPair(*pair), pair_list)

def extract_pairs(nested_list):
    """
    given list of list, extract all the pairs in the inner-list

    """
    from itertools import combinations
    
    pairs = []

    for lst in nested_list:
        pairs += make_ing_pairs(combinations(lst, 2))

    return pairs

def extract_items(nested_list):
    """
    given list of list, extract all occurrence if the inner-list items
    """
    return [i for lst in nested_list for i in lst]

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

def load_ing_prob_table_from_pickle(path):
    """
    (str) => IngProbTable
    
    given the pickle path, load the ingredient prob table
    >>> potato = "土豆".decode("utf8")
    >>> tomato = "番茄".decode("utf8")
    >>> tbl = load_ing_prob_table_from_pickle("data/douguo.recipe.pickle")
    >>> tbl.pmi(potato, tomato)
    1.0410830540710134
    """
    from cPickle import load
    return load(open(path, "r"))

def make_ing_prob_table_from_file(recipe_path):
    """(str) => IngProbTable

    make a ingredient probability table given the recipe file path
    
    >>> potato = "土豆".decode("utf8")
    >>> tomato = "番茄".decode("utf8")
    >>> tbl = make_ing_prob_table_from_file("data/douguo.recipe")
    >>> tbl.pmi(potato, tomato)
    1.0410830540710134
    """
    #load ingredients list
    ing_list = load_ing_list(recipe_path)
    return IngProbTable(ing_list)

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
        (tuple of(str, str) or str) => float
        
        return the prob of the ingredient pair or the single ingredient item
        """
        if isinstance(key, tuple):
            return self.pair_prob.get((IngredientPair(*key)), 0)
        elif isinstance(key, unicode):
            return self.item_prob.get(key, 0)
        else:
            raise KeyError("Invalid Key %s" %key.encode("utf8"))

    def pmi(self, ing1, ing2):
        """(str, str) => float
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
    tbl = make_ing_prob_table_from_file(path)
    print "made table"

    from cPickle import dump
    dump(tbl, open(path + ".pickle", "w"))
    print "to file"

def main():
    pickle_ing_prob_table("data/douguo.recipe")

def test():
    import doctest
    doctest.testmod()
    #doctest.run_docstring_examples(load_ing_gprob_table_from_pickle, globals())
    
if __name__ == "__main__":
#    test()
    main()
