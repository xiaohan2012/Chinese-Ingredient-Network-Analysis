#-!- coding=utf8 -!-
"""
Chinese word inspection module

This module rises from the question: 

Can this kind of ingredient names, 肥的猪肉，冰冻的猪肉,and so on, be shortened into a more uniform way, such as 猪肉? And how?
"""
from prob import extract_items
from source import load_ing_list

from collections import Counter
from codecs import open
from cPickle import load, dump

class WordFreqTable(Counter):
    """The Chinese word frequency table"""
    
    def __init__(self, word_list = []):
        self.word_list = word_list
        Counter.__init__(self, word_list)
                
    @classmethod
    def from_recipe_file(cls, path):
        """construct the word frequecy table from recipe file"""
        import jieba
        ingredients_list = load_ing_list()
        items = extract_items(ingredients_list)
        return cls([word for item in items for word in jieba.cut(item.encode("utf8"), cut_all=False)])

    def most_likely(self, name_list):
        """
        (list of unicode) => unicode

        select from a list of names the most representitive name,
        like '冰冻','的','猪肉' => '猪肉'
        """
        return max(name_list, key=lambda w: self[w])
    
    def to_cache(self, path="ingredients_occurence.txt"):
        """save the word occurence list to text file"""
        
        with open(path, "w", "utf8") as f:
            for w in self.word_list:
                f.write(w+"\n")
        
    @classmethod
    def from_cache(cls, path="ingredients_occurence.txt"):
        words = [l.strip() for l in open(path, "r", "utf8").readlines()]
        return WordFreqTable(words)

def test():
    import doctest
    doctest.testmod()

def main():
    #tbl = WordFreqTable.from_recipe_file("data/douguo.recipe")
    tbl = WordFreqTable.from_cache()
    for ing, freq in tbl.most_common(100):
        print ing, tbl[ing]
    #tbl.to_cache()

if __name__ == "__main__":
    main()
    #test()
