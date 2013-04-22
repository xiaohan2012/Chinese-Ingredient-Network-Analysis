#-!- coding=utf8 -!-

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
