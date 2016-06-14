# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawlerItem(scrapy.Item):
    domain = scrapy.Field()
    title  = scrapy.Field()
    description = scrapy.Field()
    body = scrapy.Field()
    h1 = scrapy.Field()
    h2 = scrapy.Field()
    url = scrapy.Field()
