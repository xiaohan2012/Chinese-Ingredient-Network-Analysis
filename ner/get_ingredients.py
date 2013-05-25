from codecs import open
from simplejson import load

def raw_ingredients(path):
    f = open(path, "r", "utf8")
    ing_list = list({ing for r in load(f) for ing in r.get("ingredients", [])})
    for ing in  sorted(ing_list, key = lambda ing: len(ing), reverse = True):
        yield ing
        
if __name__ == '__main__':
    for i in raw_ingredients("data/recipes.json"):
        print i.encode("utf8")
    #raw_ingredients("recipes.json")
