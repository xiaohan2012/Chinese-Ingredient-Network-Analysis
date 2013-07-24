#-!- coding=utf8 -!-

class UnorderedTuple(tuple):
    """in terms of ingredient pair, 
    (土豆,番茄) is the same as (番茄,土豆)"""
    
    def __new__(cls, i1, i2):
        #because tuple is immutable, use __new__
        return tuple.__new__(cls, (i1, i2))
        
    def __eq__(self, other):
        return (self[0] == other[0] and self[1] == other[1]) or (self[0] == other[1] and self[1] == other[0])
    
    def __str__(self):
        i1, i2 = sorted(list(self))
        return "%s+%s" %(i1.encode("utf8"), i2.encode("utf8"))

    def __repr__(self):
        return str(self)

    def __hash__(self):
        return hash(" ".join(sorted(list(self))))

