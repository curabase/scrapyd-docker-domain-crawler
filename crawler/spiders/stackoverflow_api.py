# -*- coding: utf-8 -*-
import scrapy


class StackoverflowApiSpider(scrapy.Spider):
    name = "stackoverflow_api"
    allowed_domains = ["stackoverflow.com"]
    start_urls = (
        'http://www.stackoverflow.com/',
    )

    def parse(self, response):
        pass
