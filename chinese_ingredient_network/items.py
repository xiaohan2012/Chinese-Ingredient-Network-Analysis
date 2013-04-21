# -!- coding=utf8 -!-

from scrapy.item import Item, Field

class Recipe(Item):

    from scrapy.contrib.loader.processor import MapCompose, Join, TakeFirst

    name = Field(output_processor=TakeFirst())
    url = Field(output_processor=TakeFirst())
    tags = Field(default=[])
    ingredients = Field()

    def __repr__(self):
        ingredient_str = u' '.join(self['ingredients'])
        return "%s\nIngredients：%s" %(self["name"].encode("utf8"), ingredient_str.encode("utf8"))
