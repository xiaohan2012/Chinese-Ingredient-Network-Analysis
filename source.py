"""Data loading utility"""
from simplejson import load

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

def main():
    for i in load_recipes():
        print i

if __name__ == "__main__":
    main()
