# -!- coding=utf8 -!-

import unittest

from word_freq import WordFreqTable

tbl = WordFreqTable.from_cache()

def to_unicode(str_list):
    return map(lambda s: s.decode("utf8"), str_list)

class WordFreqTableTest(unittest.TestCase):
    def test_most_common_one(self):
        """the most common for douguo should be salt"""
        actual = tbl.most_common(1)[0][0]
        expected = '盐'.decode("utf8")
        self.assertEqual(actual, expected)


    def test_most_likely_1(self):
        name_list = to_unicode(['猪','姜末','米饭'])
        actual = tbl.most_likely(name_list)
        expected = '猪'.decode("utf8")

        self.assertEqual(actual, expected)
        


if __name__ == "__main__":
    unittest.main()
        
        
