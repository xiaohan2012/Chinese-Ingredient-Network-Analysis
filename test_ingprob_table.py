# -!- encoding=utf8 -!-
from __future__ import division
import unittest 
import numpy as np

from prob import IngProbTable


potato = "土豆".decode("utf8")
beef = "牛肉".decode("utf8")
pepper = "辣椒".decode("utf8")
tomato = "番茄".decode("utf8")
egg = "鸡蛋".decode("utf8")
hair = "头发".decode("utf8")


class IngProbTableTestCase(unittest.TestCase):
    def setUp(self):
        ing_list = [[potato, beef, pepper], [tomato, beef], [tomato, egg], [potato, pepper]]
        self.table = IngProbTable(ing_list)


    def test_pair_prob_1(self):
        """p(potato + pepper ) = 2/4"""
        expected = 2/4
        actual = self.table[potato, pepper]
        self.assertEqual(expected, actual)

    def test_pair_prob_2(self):
        """p(tomato, egg) = 1/4"""
        expected = 1/4
        actual = self.table[egg, tomato]
        self.assertEqual(expected, actual)
        
    def test_pair_prob_3(self):
        """p(tomato, potato) = 0"""
        expected = 0
        actual = self.table[tomato, potato]
        self.assertEqual(expected, actual)

    def test_item_prob_1(self):
        """p(potato) = 2/4"""
        expected = 2/4
        actual = self.table[potato]
        self.assertEqual(expected, actual)

    def test_item_prob_2(self):
        """p(egg) = 1/4"""
        expected = 1/4
        actual = self.table[egg]
        self.assertEqual(expected, actual)        

    def test_item_prob_3(self):
        """p(egg) = 0"""
        expected = 0
        actual = self.table[hair]
        self.assertEqual(expected, actual)        

    def test_pmi_1(self):
        """pmi(beef, potato) = 0"""
        expected = 0
        actual = self.table.pmi(beef, potato)
        self.assertEqual(expected, actual)        
        
    def test_pmi_2(self):
        """pmi(tomato, potato) = -inf"""
        expected = float('-inf')
        actual = self.table.pmi( potato, tomato)
        self.assertEqual(expected, actual)        

if __name__ == "__main__":
    unittest.main()


