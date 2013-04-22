# -!- coding=utf8 -!-

import unittest

from preprocess import expand_cluttered_recipe, remove_number_and_unit, remove_anotation, make_ingredients_mapping

from source import load_recipes, load_corrected_recipe_from_file
from extract import extract_recipe_ingredient_list
from dataview import get_raw_ingredients

class ExpandClutteredRecipeTestCase(unittest.TestCase):
    """test case for expand_cluttered_recipe function"""

    def setUp(self):
        recipe_1 = {u'url': u'http://www.douguo.com/cookbook/2017.html', u'ingredients': [u'\u82e6\u74dc2\u6839 \u5c0f\u6392350\u514b', u'\u751f\u59dc3\u7247 \u8471\u4e00\u5c0f\u6bb5 \u516b\u89d22\u679a \u6599\u91522\u6c64\u5319 \u751f\u62bd2\u6c64\u5319 \u767d\u7cd61\u6c64\u5319 \u8c46\u8c491\u8336\u5319 \u76d01/2\u8336\u5319 \u6cb91\u6c64\u5319'], u'name': u'\u82e6\u74dc\u70e7\u6392\u9aa8', u'tags': [u'\u8001\u5c11\u7686\u5b9c', u'\u79c1\u5bb6\u83dc', u'\u5927\u4f17\u83dc', u'\u54b8\u9999']}
        
        self.r1 = expand_cluttered_recipe(recipe_1)

        recipe_2 = {u'url': u'http://www.douguo.com/cookbook/2283.html', u'ingredients': [u'\u732a\u6392\u80895\u7247\uff0c\u751c\u9762\u917130\u514b', u'\u6599\u9152\u3001\u6cb9\u3001\u76d0\u3001\u80e1\u6912\u7c89\u3001\u5b5c\u7136\u7c89\u3001\u6c34\u6dc0\u7c89'], u'name': u'\u7b80\u6613\u7248\u7684\u714e\u732a\u6392 \u9171\u6c41\u732a\u6392', u'tags': [u'\u8001\u5c11\u7686\u5b9c', u'\u732a\u8089', u'\u5927\u4f17\u83dc', u'\u54b8']}
        
        self.r2 = expand_cluttered_recipe(recipe_2)

    def test_dict_length_case_1(self):
        """ test recipe 1, dict length should equal to 4"""
        self.assertEqual(len(self.r1.keys()), 4)    
        
    def test_dict_length_case_2(self):
        """ test recipe 2, dict length should equal to 4"""
        self.assertEqual(len(self.r2.keys()), 4)    

    def test_ingredients_case_1(self):
        """space separated case"""
        self.assertEqual(self.r1["ingredients"], [u'\u82e6\u74dc2\u6839', u'\u5c0f\u6392350\u514b', u'\u751f\u59dc3\u7247', u'\u8471\u4e00\u5c0f\u6bb5', u'\u516b\u89d22\u679a', u'\u6599\u91522\u6c64\u5319', u'\u751f\u62bd2\u6c64\u5319', u'\u767d\u7cd61\u6c64\u5319', u'\u8c46\u8c491\u8336\u5319', u'\u76d01/2\u8336\u5319', u'\u6cb91\u6c64\u5319'])
        
    def test_ingredients_case_2(self):
        """ 、separated case"""
        self.assertEqual(self.r2["ingredients"], [u'\u732a\u6392\u80895\u7247\uff0c\u751c\u9762\u917130\u514b', u'\u6599\u9152', u'\u6cb9', u'\u76d0', u'\u80e1\u6912\u7c89', u'\u5b5c\u7136\u7c89', u'\u6c34\u6dc0\u7c89'])


class RemoverTestCase(unittest.TestCase):
    def test_remove_number_and_unit(self):
        """test for remove_number_and_unit"""
        self.assertEqual(remove_number_and_unit(u"玉米粉12克"),u"玉米粉")


    def test_remove_number_and_unit_unchanged(self):
        """the string should be left unchanged"""
        self.assertEqual(remove_number_and_unit(u"玉米粉"), u"玉米粉")

    def test_remove_anotation(self):
        """test for remove_anotation"""
        self.assertEqual(remove_anotation(u"淀粉（适量即可）"), u"淀粉")

    def test_remove_annotation_case_2(self):
        self.assertEqual(remove_anotation(u"哈蜜瓜（黄瓤）160g"), u"哈蜜瓜")

    def test_remove_anotation_unchanged(self):
        """test for remove_anotation, the string should be left unchanged"""
        self.assertEqual(remove_anotation(u"淀粉"), u"淀粉")

    def test_joint_case(self):
        """remove_number_and_unit and remove_annotation are composed"""
        self.assertEqual(remove_anotation(remove_number_and_unit(u"哈蜜瓜（黄瓤）160g")), u"哈蜜瓜")

        
class IngredientMappingTestCase(unittest.TestCase):
    def setUp(self):

        recipes = load_recipes()
        ings = get_raw_ingredients(recipes)
        self.m = make_ingredients_mapping(ings)
        
    def test_mapping_type(self):
        """the mapping should be a dict"""
        self.assertTrue(isinstance(self.m, dict))
        
    def test_difference(self):
        """the key and value in each pair should be different"""
        k = self.m.keys()[0]
        v = self.m[k]
        self.assertNotEqual(k,v)

    def test_content_case_1(self):
        """test if their correction are correct as expected"""
        key = u"鸡腿1个"
        expected = u"鸡腿"
        self.assertEqual(expected, self.m[key])

    def test_content_case_2(self):
        """test if their correction are correct as expected"""
        key = u"菩提花1/2匙"
        expected = u"菩提花"
        actual = self.m[key]
        self.assertEqual(expected, actual)

    def test_content_case_3(self):
        """test if their correction are correct as expected"""
        key = u"哈蜜瓜（黄瓤）160g"
        expected = u"哈蜜瓜"
        actual =  self.m[key]
        self.assertEqual(expected, actual)

    def test_content_case_4(self):
        """test if their correction are correct as expected"""
        key = u"水淀粉1汤匙（15ml）"
        expected = u"水淀粉"
        self.assertEqual(expected, self.m[key])

    def test_content_case_5(self):
        """test if their correction are correct as expected"""
        key = u"A.绞肉400g"
        expected = u"A.绞肉"
        self.assertEqual(expected, self.m[key])

class IngredientNameCorrectionTestCase(unittest.TestCase):
    def setUp(self):
        old_recipes = load_recipes()
        self.old_ings = get_raw_ingredients(old_recipes)
        self.recipes = load_corrected_recipe_from_file()

    def test_ingredient_count_reduction(self):
        """after correction, the ingredient count should outnumber """
        new_ings = get_raw_ingredients(self.recipes)

        self.assertGreater(len(self.old_ings), len(new_ings))

class IngredientListExtractionTestCase(unittest.TestCase):
    """test for extracting ingredient list"""

    def test_ingredient_list_length(self):
        """ingredient list length should = recipe length"""
        recipes = load_corrected_recipe_from_file()
        ing_list = extract_recipe_ingredient_list(recipes)

        self.assertEqual(len(recipes), len(ing_list))


if __name__ == "__main__":
    unittest.main()
    
