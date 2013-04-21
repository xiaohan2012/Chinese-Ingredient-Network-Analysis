# -!- coding=utf8 -!-
from __future__ import division

from preprocess import *

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
    from collections import Counter, defaultdict
    pair_freq = Counter(pair_list)
    item_freq = Counter(item_list)
    
    #ingredient pair prob table
    pair_prob = defaultdict(int)
    for pair, freq in pair_freq.items():
        pair_prob[pair] = freq / recipe_count
        
    #ingredient item prob table
    item_prob = defaultdict(int)
    for item, freq in item_freq.items():
        item_prob[item] = freq / recipe_count

    return pair_prob, item_prob
    
    
if __name__ == "__main__":
    import doctest
    doctest.testmod()
