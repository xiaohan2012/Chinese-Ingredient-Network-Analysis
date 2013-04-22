# -!- coding=utf8 -!-

from source import load_recipes

def get_raw_ingredients(recipes):
    """
    (list of dict) => list of str
    
    given the recipe list, return all the ingredients(raw string from the crawling result)
    
    >>> recipes = load_recipes()
    >>> ings = get_raw_ingredients(recipes)
    >>> type(ings)
    <type 'set'>
    >>> len(ings)
    48110
    """

    return set([ing for rec in recipes for ing in rec[u"ingredients"]])

def m_to_n_ings(m,n, ings):
    return list(ings)[m:n]

def first_n_ings(n, ings):
    return m_to_n_ings(0,n,ings)


def test():
    import doctest
    doctest.testmod()

def main():
    recipes = load_recipes()
    ings = get_raw_ingredients(recipes)
    print "\n".join(map(lambda s:s.encode("utf8"),first_n_ings(100, ings)))


if __name__ == "__main__":
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        test()
    else:
        main()
