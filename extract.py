#-!- coding=utf8 -!-

from recipe import Ingredient, IngredientPair

def extract_pairs(nested_list):
    """
    given list of list, extract all the pairs in the inner-list

    """
    def make_ing_pairs(pair_list):
        """(list of tuple) => list of IngredientPair
        >>> i1 = Ingredient("土豆")
        >>> i2 = Ingredient("番茄")
        >>> i3 = Ingredient("鸡蛋")
        >>> ing_list = make_ing_pairs([(i1,i2),(i2,i1),(i2,i3)])
        >>> print ing_list
        [土豆 + 番茄, 土豆 + 番茄, 番茄 + 鸡蛋]
        """
        return map(lambda pair: IngredientPair(*pair), pair_list)

    from itertools import combinations
    
    pairs = []

    for lst in nested_list:
        pairs += make_ing_pairs(combinations(lst, 2))

    return pairs

def extract_items(nested_list):
    """
    (list of list of Ingredients) => list of Ingredients

    given list of list, extract all occurrence if the inner-list items
    """
    return [Ingredient(i) for lst in nested_list for i in lst]


def extract_recipe_ingredient_list(recipes):
    """
    (list of recipe dict) => list of ingredient list
    
    given the recipes, return a nested list of ingredients
    for example, [["土豆","萝卜"], ["番茄","鸡蛋"], ...]
    """
    return map(lambda r: r["ingredients"], recipes)



def test():
    import doctest
    doctest.testmod()
    
if __name__ == "__main__":
    test()
