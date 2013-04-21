# -!- coding=utf8 -!-

from scrapy.selector import HtmlXPathSelector
from scrapy.contrib.linkextractors.sgml import SgmlLinkExtractor
from scrapy.contrib.spiders import CrawlSpider, Rule
from chinese_ingredient_network.items import Recipe

class DouguoSpider(CrawlSpider):
    name = 'douguo'
    allowed_domains = ['douguo.com']
    start_urls = [u'http://www.douguo.com/caipu/川菜',
                  u'http://www.douguo.com/caipu/湘菜',
                  u'http://www.douguo.com/caipu/鲁菜',
                  u'http://www.douguo.com/caipu/粤菜',
                  u'http://www.douguo.com/caipu/东北菜']

    rules = (
        Rule(SgmlLinkExtractor(allow=r'cookbook/.*.html'), callback = 'parse_recipe', follow=True),
    )
        
    download_delay = 0.1
    


    def parse_recipe(self, response):
        """
        @url http://www.douguo.com/cookbook/215296.html
        @returns items 1
        @scrapes name url ingredients

        @url http://www.douguo.com/cookbook/190309.html
        @returns items 1
        @scrapes name url ingredients
        
        @url http://www.douguo.com/cookbook/211633.html
        @returns items 1
        @scrapes name url tags ingredients
        """

        from pyquery import PyQuery as pq
        from scrapy.contrib.loader import ItemLoader

        doc = pq(response.body)
        l = ItemLoader(item = Recipe())
        
        l.add_value("name",  doc("#page_cm_id").text())
        l.add_value("url", response.url)
        l.add_value("tags", [pq(s).text() for s in doc('#displaytag span')])
        
        def ingredients():
            """get the ingredients"""
            mtims = doc(".mtim")
            trs = mtims.eq(0).siblings()
            
            get_list = lambda iters: [pq(td)("span").eq(0).text() for tr in iters for td in pq(tr)("td") if len(pq(td).children("span")) > 0]
            
            return get_list(trs)

        l.add_value("ingredients", ingredients())
        
        return l.load_item()
