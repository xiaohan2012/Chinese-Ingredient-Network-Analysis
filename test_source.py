# -!- coding=utf8 -!-

import unittest

from source import load_recipes

class LoadingRecipeTestCase(unittest.TestCase):
    """test case for load_recipes function"""
    def setUp(self):
        self.r = load_recipes()

    def test_length(self):
        """recipe count test"""
        self.assertEqual(47973, len(self.r))

    def test_the_first_element(self):
        """test the content matching of the first element"""
        self.assertEqual(self.r[0], {u'url': u'http://www.douguo.com/cookbook/205892.html', u'ingredients': [u'\u91cc\u810a\u8089', u'\u9e21\u86cb\u6e05', u'\u6c34\u6dc0\u7c89', u'\u918b', u'\u767d\u7802\u7cd6', u'\u756a\u8304\u9171', u'\u80e1\u6912', u'\u76d0', u'\u5473\u7cbe', u'\u59dc\u672b', u'\u849c\u672b', u'\u719f\u829d\u9ebb'], u'name': u'\u5341\u6b65\u505a\u51fa\u9999\u9165\u7cd6\u918b\u91cc\u810a', u'tags': [u'\u5bb6\u5e38\u83dc', u'\u7cd6\u918b\u5473']})


if __name__ == "__main__":
    unittest.main()
