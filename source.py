#-!- coding=utf8 -!-

"""Data loading utility"""
from simplejson import load

from recipe import Ingredient, IngredientPair
from extract import extract_recipe_ingredient_list
from prob import IngProbTable

def load_recipes(file="data/douguo.recipe"):
    """
    str => dict
    
    load the recipe json file, and perform the following preprocessing:
    1, filter out recipes without ingredients
    2, perform necessary expansion on recipe ingredients

    """
    def has_ingredients(recipe):
        """if the recipe has `ingredients` key"""
        return "ingredients" in recipe.keys()
    
    from codecs import open
    from preprocess import expand_cluttered_recipe
    
    return map(expand_cluttered_recipe, filter(has_ingredients, load(open(file, 'r', 'utf8'))))

def load_corrected_recipe_from_file(path="data/douguo.recipe"):
    """
    (str) => list of dict

    load the recipe, correct the names and return the corrected recipe
    """
    from preprocess import make_ingredients_mapping, correct_ingredient_names

    from dataview import get_raw_ingredients

    #loading recipe
    recipes = load_recipes(path)
    
    #get raw ingredients
    ings = get_raw_ingredients(recipes)
    
    #make the name correction map
    mapping = make_ingredients_mapping(ings)
    
    #correct the ingredient names according to the map
    recipes = correct_ingredient_names(recipes, mapping)
    
    #return the corrected recipes
    return recipes


def load_ing_list(path="data/douguo.recipe"):
    """load the ingredient list, in forms ogf [[a,b],[c,d,e]]"""

    recipes = load_corrected_recipe_from_file(path)
    ing_list = extract_recipe_ingredient_list(recipes)
    return ing_list

def load_ing_prob_table_from_pickle(path):
    """
    (str) => IngProbTable
    
    given the pickle path, load the ingredient prob table
    >>> potato = Ingredient("土豆")
    >>> tomato = Ingredient("番茄")
    >>> tbl = load_ing_prob_table_from_pickle("data/test/douguo.pickle")
    >>> tbl.pmi(potato, tomato)
    0.77576979506792032
    """
    from cPickle import load

    return load(open(path, "r"))

def load_ing_prob_table_from_file(recipe_path):
    """(str) => IngProbTable

    make a ingredient probability table given the recipe file path
    
    >>> potato = Ingredient("土豆")
    >>> tomato = Ingredient("番茄")
    >>> tbl = load_ing_prob_table_from_file("data/test/douguo.recipe")
    >>> tbl.pmi(potato, tomato)
    0.77576979506792032
    """
    #load ingredients list
    ing_list = load_ing_list(recipe_path)
    return IngProbTable(ing_list)


def main():
    for i in load_recipes():
        print i

def test():
    import doctest
    doctest.testmod()


if __name__ == "__main__":
#    main()
    test()
