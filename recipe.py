#-!- coding=utf8 -!-

class Recipe(dict):
    """Recipe class"""
    @classmethod
    def from_dict(cls, d):
        """(dict) => Recipe"""
        obj = cls(d)
        
        obj.ingredients = IngredientList(map(Ingredient, obj.unclutter().ingredients))
        
        return obj

    def __getattr__(self, key):
        return self[key]
    
    def __setattr__(self, key, value):
        return self[key]
    
    def __str__(self):
        return "%s: %s" %(self.name, self.ingredients)

    def unclutter(self):
        """
        (Recipe) => Recipe
        some recipe might have ingredients like 生姜3片 葱一小段 八角2枚 料酒2汤匙 生抽2汤匙 白糖1汤匙 豆豉1茶匙 盐1/2茶匙 油1汤匙
        OR 酒、油、盐、胡椒粉、孜然粉、水淀粉
        
        In this case, the ingredient should be expanded into smaller parts
        """
        from deepcopy import copy
            #copy the result
        new_recipe = copy(recipe)
        
            #uncluttered ingredient list
        ings = []
        for ing in new_recipe.ingredients:
            ings += re.split(u"[ \u3001]+", ing)
            new_recipe["ingredients"] = ings
        return new_recipe

from codecs import open

class RecipeList(list):
    """List of Recipe"""
    
        
    @classmethod
    def from_json_file(cls, path):
        def has_ingredients(recipe):
            """if the recipe has `ingredients` key"""
            return "ingredients" in recipe.keys()
    
        from preprocess import expand_cluttered_recipe
        
        recipes = map(Recipe, load(open(file, 'r', 'utf8')))
        with_ingredient_recipes = filter(has_ingredients, recipes)
        unclutered_recipes = map(lambda r: r.unclutter(), with_ingredient_recipes)

        return unclutered_recipes
        
    def ingredients_set(self):
        """unique ingredient names"""
        return set([ing for recipe in recipes for ing in recipe["ingredients"]])

class Ingredient(unicode):
    """wrapper class for Ingredient
    
    >>> i = Ingredient("土豆")
    >>> print(i.encode("utf8"))
    土豆
    """

    def __new__(cls, name):
        if not isinstance(name, unicode):#not unicode, convert it to unicode
            name = name.decode("utf8")
        return unicode.__new__(cls, name)

class IngredientList(list):
    """
    a list of ingredients

    >>> potato = Ingredient("土豆")
    >>> tomato = Ingredient("番茄")
    >>> beef = Ingredient("牛肉")
    >>> lst = IngredientList(potato, tomato, beef)
    >>> print lst.possible_pairs()
    土豆+番茄 土豆+牛肉 番茄+牛肉
    """
    def possible_pairs(self):
        """all possible pair of ingredients from a ingredient list"""
        from itertools import combinations
        return combinations(self, 2)
    
    def __str__(self):
        return " ".join(self)

class IngredientPair(tuple):
    """class for ingredient pair
    
    >>> potato = Ingredient("土豆")
    >>> tomato = Ingredient("番茄")
    >>> p1 = IngredientPair(potato, tomato)
    >>> p2 = IngredientPair(tomato, potato)
    >>> p1 == p2 #test for object equality
    True
    >>> len(set([p1,p2])) #p1 and p2 should be considered identical in a set
    1
    >>> print p1
    土豆+番茄
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
        return "%s+%s" %(i1.encode("utf8"), i2.encode("utf8"))

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(" ".join(sorted(list(self))))

if __name__ == "__main__":
    import doctest
    doctest.testmod()
