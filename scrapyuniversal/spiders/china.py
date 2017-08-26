# -*- coding: utf-8 -*-
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapyuniversal.items import *
from scrapyuniversal.loaders import *


class ChinaSpider(CrawlSpider):
    name = 'china'
    allowed_domains = ['tech.china.com']
    start_urls = ['http://tech.china.com/articles/']
    
    rules = (
        Rule(LinkExtractor(allow='article\/.*\.html', restrict_xpaths='//div[@id="left_side"]//div[@class="con_item"]'),
             callback='parse_item'),
        Rule(LinkExtractor(restrict_xpaths='//div[@id="pageStyle"]//a[contains(., "下一页")]'))
    )
    
    def parse_item(self, response):
        l = ChinaLoader(item=NewsItem(), response=response)
        l.add_xpath('title', '//h1[@id="chan_newsTitle"]/text()')
        l.add_value('url', response.url)
        l.add_xpath('text', '//div[@id="chan_newsDetail"]//text()')
        l.add_xpath('datetime', '//div[@id="chan_newsInfo"]/text()', **{'re': '(\d+-\d+-\d+\s\d+:\d+:\d+)'})
        l.add_xpath('source', '//div[@id="chan_newsInfo"]/text()', **{'re': '来源：(.*)'})
        l.add_value('website', '中华网')
        return l.load_item()
