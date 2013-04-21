# -!- coding=utf8 -!-
from __future__ import division

import unittest

from graph import *

class IngredientPairExtractionTestCase(unittest.TestCase):
    """test for extracting ingredient pairs"""

    def test_extract_pairs(self):
        """test for extracting pairs from list of list"""
        ing_list = [(1,2,3),(4,5),(1,2),(6,)]
        actual = extract_pairs(ing_list)
        expected = map(lambda pair: IngredientPair(*pair), [(1,2),(1,3),(2,3),(4,5),(1,2)])

        self.assertEqual(actual, expected)
        
    def test_ing_pair_in_list_case_1(self):
        """test for extracting ingredient pairs"""
        ing_list = load_ing_list()
        pairs = extract_pairs(ing_list)

        ing1 = "排骨".decode("utf8")
        ing2 = "萝卜".decode("utf8")

        self.assertTrue(IngredientPair(ing1, ing2) in pairs)
        self.assertTrue(IngredientPair(ing2, ing1) in pairs)

    def test_ing_pair_in_list_case_2(self):
        """test for extracting ingredient pairs"""

        ing_list = load_ing_list()
        pairs = extract_pairs(ing_list)

        ing1 = "土豆".decode("utf8")
        ing2 = "酱油".decode("utf8")

        self.assertTrue(IngredientPair(ing1, ing2) in pairs)

class IngredientsExtractionTestCase(unittest.TestCase):
    """Test for extracting occurences of ingredients"""

    def test_ing_item_in_list_case_1(self):
        """test for extracting ingredient items"""

        ing_list = load_ing_list()
        pairs = extract_items(ing_list)

        ing = "土豆".decode("utf8")

        self.assertTrue(ing in pairs)

class MakeProbTableTestCase(unittest.TestCase):
    def test_simple_case_pair_prob(self):
        """ """
        recipe_count = 3
        potato = "土豆".decode("utf8")
        tomato = "番茄".decode("utf8")
        egg = "鸡蛋".decode("utf8")
        honey = "蜂蜜".decode("utf8")

        pair_list = make_ing_pairs([(potato,tomato),(tomato,potato),(tomato,egg)])

        item_list = [potato, tomato, tomato, potato, tomato, egg]
        pair_prob, item_prob = make_prob_table(pair_list, item_list, recipe_count)

        self.assertEqual(pair_prob[IngredientPair(potato, tomato)], 2/3)
        self.assertEqual(pair_prob[IngredientPair(tomato, potato)], 2/3)
        self.assertEqual(pair_prob[IngredientPair(tomato, egg)], 1/3)
        
        #impossible case
        self.assertEqual(pair_prob[IngredientPair(honey, egg)], 0)

        
    def test_simple_case_item_prob(self):
        recipe_count = 3
        potato = "土豆".decode("utf8")
        tomato = "番茄".decode("utf8")
        egg = "鸡蛋".decode("utf8")
        honey = "蜂蜜".decode("utf8")
        
        pair_list = make_ing_pairs([(potato,tomato),(tomato,potato),(tomato,egg)])

        item_list = [potato, tomato, tomato, potato, tomato, egg]
        pair_prob, item_prob = make_prob_table(pair_list, item_list, recipe_count)

        self.assertEqual(item_prob[potato], 2/3)
        self.assertEqual(item_prob[tomato], 1)
        self.assertEqual(item_prob[egg], 1/3)
        
        #impossible case
        self.assertEqual(item_prob[honey], 0)
        

if __name__ == "__main__":
    unittest.main()
