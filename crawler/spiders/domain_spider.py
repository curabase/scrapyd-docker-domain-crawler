import scrapy

from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from crawler.items import CrawlerItem
from urllib.parse import urlparse

import lxml.etree
import lxml.html


class DomainSpider(CrawlSpider):
    name = "domain_spider"

    def __init__(self, url=None, allowed=None, es_server='http://elasticsearch:9200', es_index='crawl_index', **kwargs):

        self.start_urls = ['{}'.format(url)]
        self.allowed_domains = [urlparse(url).netloc]
        self.domain = urlparse(url).netloc
        self.rules = (
            Rule( LinkExtractor(allow=(allowed), unique=True, ), follow=True, callback='parse_page' ),
        )
        super(DomainSpider, self).__init__(**kwargs)


    def strip_html(self, body):
        # http://stackoverflow.com/a/17727287/1646663

        root = lxml.html.fromstring(body)
        lxml.etree.strip_elements(root, lxml.etree.Comment, "script", "head","style")
        tmpstr = lxml.html.tostring(root, method="text", encoding='unicode')
        return ' '.join(tmpstr.split())

    def parse_page(self, response):
        i = CrawlerItem()
        i['domain'] = urlparse(response.url).netloc
        i['title'] = ''.join(response.css('title::text').extract())
        i['description'] = ''.join(response.css('meta[name="description"]::attr("content")').extract())
        i['body'] = self.strip_html(response.body)
        i['url'] = response.url

        return i
