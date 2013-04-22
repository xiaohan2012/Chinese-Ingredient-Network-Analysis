# -!- coding=utf8 -!-
from __future__ import division

import unittest

from recipe import IngredientPair, Ingredient


from prob import make_prob_table


potato = Ingredient("土豆")
tomato = Ingredient("番茄")
egg = Ingredient("鸡蛋")
honey = Ingredient("蜂蜜")


class MakeProbTableTestCase(unittest.TestCase):
    def test_simple_case_pair_prob(self):
        """ """
        recipe_count = 3

        pair_list = map(lambda s: IngredientPair(*s), [(potato,tomato),(tomato,potato),(tomato,egg)])

        item_list = [potato, tomato, tomato, potato, tomato, egg]
        pair_prob, item_prob = make_prob_table(pair_list, item_list, recipe_count)

        self.assertEqual(pair_prob[IngredientPair(potato, tomato)], 2/3)
        self.assertEqual(pair_prob[IngredientPair(tomato, potato)], 2/3)
        self.assertEqual(pair_prob[IngredientPair(tomato, egg)], 1/3)
        
        #impossible case
        self.assertEqual(pair_prob.get(IngredientPair(honey, egg), 0), 0)

        
    def test_simple_case_item_prob(self):
        recipe_count = 3
        
        pair_list = map(lambda pair: IngredientPair(*pair), [(potato,tomato),(tomato,potato),(tomato,egg)])

        item_list = [potato, tomato, tomato, potato, tomato, egg]
        pair_prob, item_prob = make_prob_table(pair_list, item_list, recipe_count)

        self.assertEqual(item_prob[potato], 2/3)
        self.assertEqual(item_prob[tomato], 1)
        self.assertEqual(item_prob[egg], 1/3)
        
        #impossible case
        self.assertEqual(item_prob.get(honey, 0), 0)
        

if __name__ == "__main__":
    unittest.main()
