# -!- coding=utf8 -!-

import re

def expand_cluttered_recipe(recipe):
    """
    (dict) => dict
    some recipe might have ingredients like 生姜3片 葱一小段 八角2枚 料酒2汤匙 生抽2汤匙 白糖1汤匙 豆豉1茶匙 盐1/2茶匙 油1汤匙
    OR 酒、油、盐、胡椒粉、孜然粉、水淀粉

    In this case, the ingredient should be expanded into smaller parts
    """
    new_d = dict(recipe)
    ings = []
    for ing in new_d["ingredients"]:
        ings += re.split(u"[ \u3001]+", ing)

    new_d["ingredients"] = ings
    return new_d
    

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

def make_ingredients_mapping(ingredients, funcs = [remove_anotation, remove_number_and_unit]):
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

def print_correction_dictionary(dictionary):
    for original, corrected in dictionary.items():
        print(original, corrected)

        
def main():
    recipes = load_corrected_recipe_from_file()
    ing_list = extract_recipe_ingredient_list(recipes)
    for i in ing_list:
        print ' '.join(i)

if __name__ == "__main__":
    main()

