# -!- coding=utf8 -!-
from __future__ import division

import unittest

from recipe import IngredientPair, Ingredient

from source import load_ing_list
from extract import extract_pairs, extract_items

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

        ing1 = Ingredient("排骨")
        ing2 = Ingredient("萝卜")

        self.assertTrue(IngredientPair(ing1, ing2) in pairs)
        self.assertTrue(IngredientPair(ing2, ing1) in pairs)

    def test_ing_pair_in_list_case_2(self):
        """test for extracting ingredient pairs"""

        ing_list = load_ing_list()
        pairs = extract_pairs(ing_list)

        ing1 = Ingredient("土豆")
        ing2 = Ingredient("酱油")

        self.assertTrue(IngredientPair(ing1, ing2) in pairs)

class IngredientsExtractionTestCase(unittest.TestCase):
    """Test for extracting occurences of ingredients"""

    def test_ing_item_in_list_case_1(self):
        """test for extracting ingredient items"""

        ing_list = load_ing_list()
        pairs = extract_items(ing_list)

        ing = Ingredient("土豆")

        self.assertTrue(ing in pairs)

if __name__ == "__main__":
    unittest.main()
