#-!- coding=utf8 -!-

def load_ingredients():
    """
    >>> ings = load_ingredients()
    >>> len(ings)
    1392
    """
    file_names = ["bird.json", "meat.json", "vegetable.json", "cereal.json", "bean.json","diary.json", "noodle.json", "fruit.json", "dish.json", "aqua.json", "condiment.json"]
    
    from simplejson import load
    from codecs import open
    
    return reduce(lambda l,f: l.union(load(open("data/%s" %f, "r", "utf8"))) , file_names, set())

def create_custom_dict(freq = 10):
    """for better word segmentation, we need custom dict"""
    ings = load_ingredients()

    for ing in ings:
        print "%s %d" %(ing.encode("utf8"), freq)
        
def get_recipe_ingredients(recipe_path, user_dict_path = "data/user_dict.txt", ingredient_set = load_ingredients()):
    """
    get ingredients from recipe source file
    """
    from simplejson import load
    
    recipes = load(open(recipe_path, "r"))
    
    import jieba

    jieba.load_userdict(user_dict_path)

    return [
        [
            ing
            for sent in recipe.get("ingredients", []) #get each sentence
            for ing in filter(lambda i: i in ingredient_set, jieba.cut_for_search(sent)) #cut the sentence and filter out the interesting ingredient name
        ]
        for recipe in recipes
    ]

def load_ingredient_category_mapping():
    """
    return the ingredient to category mapping

    >>> m = ingredient_category_mapping()
    >>> m["虾仁".decode("utf8")]
    'aqua'
    >>> m["绿豆芽".decode("utf8")]
    'bean'
    """
    file_names = ["bird.json", "meat.json", "vegetable.json", "cereal.json", "bean.json","diary.json", "noodle.json", "fruit.json", "dish.json", "aqua.json", "condiment.json"]

    from simplejson import load
    from codecs import open
    
    return dict( ( (ing, fname.split(".")[0])
                   for fname in file_names
                   for ing in load(open("data/"+fname, "r", "utf8"))) )
    
def main():
    #create_custom_dict()

    ris = get_recipe_ingredients("data/douguo.recipe")
    from simplejson import dump
    dump(ris, open("data/recipe-ingredients.json", "w"))

def test():
    import doctest
    doctest.testmod()
    
if __name__ == '__main__':
    #main()
    test()