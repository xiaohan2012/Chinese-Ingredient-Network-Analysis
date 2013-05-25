# -!- coding=utf8 -!-

import re
from source import load_corrected_recipe_from_file


def remove_number_and_unit(raw_str):
    """
    remove the number and unit, for example:
    玉米粉12克 => 玉米粉
    """
    return re.split(r"\d+",raw_str)[0]

def remove_anotation(raw_str):
    """
    remove the annotion in the parenthesis
    淀粉（适量即可） => 淀粉
    """
    return re.split("（".decode("utf8"),raw_str)[0]

class LessLikelyWordRemover(object):
    """remove the less likely parts of an ingredient string"""
    def __init__(self):
        from word_freq import WordFreqTable
        self.tbl = WordFreqTable.from_cache()

    def __call__(self, string):
        """
        (str) => str
        cut the string, select the most probable part
        """
        import jieba
        str_list = list(jieba.cut(string, cut_all = False))
        return self.tbl.most_likely(str_list)

def make_ingredients_mapping(ingredients, funcs = [LessLikelyWordRemover()]):
    """(list of str, list of (str=>str)) => dict of str -> str
   
    given the ingredient raw strings and mapping functions
    return a map that maps the oringinal ingredient names to the processed names
    
    if the original name equals to the mapped name, the entry will be omitted in the map
    
    """
    def chained_func(string):
        """function calling pipeline"""
        for func in funcs:
            string = func(string)
        return string
    
    #create mapping
    mapping = {}
    
    for ing in ingredients:
        if ing.strip():#prevent empty string
            new_ing = chained_func(ing) 
            if ing != new_ing:#ensures the ingredient we recorded needs to be changed
                mapping[ing] = new_ing
            
    return mapping

def correct_ingredient_names(recipes, correction_dict):
    """
    (list of dict, dict of str->str) => list of dict

    given the recipe list and the recipe name correction dictionary, correct the ingredients names and return a new recipe list
    """
    #correct one single recipe function
    def correct_recipe(recipe):
        new_r = dict(recipe)
        new_r["ingredients"] = map(lambda s: correction_dict[s] if correction_dict.has_key(s) else s, 
                                   recipe["ingredients"])
        return new_r

    #correct all recipes
    return map(correct_recipe, recipes)

def inspect_correction_dictionary():
    from source import load_recipes

    dictionary = make_ingredients_mapping(load_recipes())
    
    for original, corrected in dictionary.items():
        print(original, corrected)
        
def main():
    from extract import extract_recipe_ingredient_list
    recipes = load_corrected_recipe_from_file()
    ing_list = extract_recipe_ingredient_list(recipes)
    for i in ing_list:
        print ' '.join(i)

if __name__ == "__main__":
    #main()
    inspect_correction_dictionary()

