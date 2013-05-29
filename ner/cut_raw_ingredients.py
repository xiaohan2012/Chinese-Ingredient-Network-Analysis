import jieba
from codecs import open

def cut(path):
    """(ingredient path: str) -> list of list of str"""
    for l in open(path, "r", "utf8"):
        words = jieba.cut(l, cut_all=False)
        yield list(words)[:-1]


if __name__ == '__main__':
    """
    for words in cut("data/ingredients-1-3500.raw"):
        print u"  ".join(words).encode("utf8")
    """
    from simplejson import dump
    words_list = list(cut("data/ingredients-1-3500.raw"))
    dump(words_list, open("data/ingredients3500.json", "w", "utf8"))