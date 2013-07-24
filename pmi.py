#-!- coding=utf8 -!-

from __future__ import division
from utuple import UnorderedTuple

def coexist_pairs(recipe_ingredients):
    """
    given the recipe ingredients, return all coexisting pairs
    >>> from simplejson import load
    >>> prs = coexist_pairs(load(open("data/recipe-ingredients.json")))
    >>> print prs[:10]
    [里脊+鸡蛋, 里脊+鸡蛋清, 淀粉+里脊, 醋+里脊, 白砂糖+里脊, 番茄+里脊, 番茄酱+里脊, 胡椒+里脊, 盐+里脊, 味精+里脊]
    """
    from itertools import combinations
    
    return [UnorderedTuple( *pair ) for ingredients in recipe_ingredients for pair in combinations(ingredients, 2)]

def ingredient_occurence(recipe_ingredients):
    """
    get all ingredient occurences
    
    >>> from simplejson import load
    >>> occ = ingredient_occurence(load(open("data/recipe-ingredients.json")))
    >>> print " ".join(occ[:10]).encode("utf8")
    里脊 鸡蛋 鸡蛋清 淀粉 醋 白砂糖 番茄 番茄酱 胡椒 盐
    """
    return [ingredient for ingredients in recipe_ingredients for ingredient in ingredients]

def build_pmi(recipe_ingredients):
    """
    return a function that represents the PMI

    >>> from simplejson import load
    >>> from utuple import UnorderedTuple
    >>> pmi_dict = build_pmi(load(open("data/recipe-ingredients.json")))
    
    """
    
    from collections import Counter
    import math
    
    prs = coexist_pairs(recipe_ingredients)
    ing_occ = ingredient_occurence(recipe_ingredients)

    ings = set(ing_occ)
    
    pc = Counter(prs)
    ic = Counter(ing_occ)

    recipe_count = len(recipe_ingredients)
    
    pmi_dict = {}
    
    for ing1 in ings:
        for ing2 in ings:
            pair = UnorderedTuple(ing1, ing2)
            if pc[pair] > 0:
                pmi_dict[pair] = pc[pair] / ic[ing1] / ic[ing2]
        
    return pmi_dict

def main():
    from simplejson import load
    from cPickle import dump
    pmi = build_pmi(load(open("data/recipe-ingredients.json")))

    dump(pmi, open("data/pmi.pickle", "w"))
    
def test():
    import doctest
    doctest.testmod()
    
if __name__ == '__main__':
    main()
    #test()    