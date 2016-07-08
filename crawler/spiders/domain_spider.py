from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor

from crawler.items import CrawlerItem
from urlparse import urlparse

import lxml.etree
import lxml.html

import requests
import logging

import pika
import os


class DomainSpider(CrawlSpider):
    name = "domain_spider"

    def __init__(self,
                 url=None,
                 batch_id=None,
                 categories=['default'],
                 allowed=None,
                 denied=None,
                 single_page=False,
                 scheduled_crawl_id=None,
                 **kwargs):

        self.categories = categories
        self.batch_id = batch_id
        self.scheduled_crawl_id = scheduled_crawl_id

        follow = True

        if allowed == '':
            allowed = None

        if denied == '':
            denied = None

        if single_page is not False and single_page != '':
            denied = '.*'
            follow = False

        self.start_urls = ['{}'.format(url)]
        self.allowed_domains = [urlparse(url).netloc]
        self.domain = urlparse(url).netloc
        self.rules = (
            Rule( LinkExtractor(allow=allowed, deny=denied, unique=True,), callback='parse_page', follow=follow),
        )

        super(DomainSpider, self).__init__(**kwargs)

        self.rmq = pika.BlockingConnection(pika.ConnectionParameters(host=os.getenv('RABBITMQ_HOST', 'rabbitmq')))
        self.channel = self.rmq.channel()
        self.channel.queue_declare('page_publish', durable=True)


    def strip_html(self, body):
        # http://stackoverflow.com/a/17727287/1646663

        root = lxml.html.fromstring(body)
        lxml.etree.strip_elements(root, lxml.etree.Comment, "script", "head","style")
        tmpstr = lxml.html.tostring(root, method="text", encoding='unicode')
        return ' '.join(tmpstr.split())

    def parse_start_url(self, response):
        return self.parse_page(response)

    def parse_page(self, response):
        i = CrawlerItem()
        i['domain'] = urlparse(response.url).netloc
        i['title'] = ''.join(response.css('title::text').extract())
        i['description'] = ''.join(response.css('meta[name="description"]::attr("content")').extract())
        i['body'] = self.strip_html(response.body)
        i['h1'] = ' '.join(response.css('h1::text').extract()).strip()
        i['h2'] = ' '.join(response.css('h2::text').extract()).strip()
        i['url'] = response.url
        i['categories'] = self.categories
        i['batch_id'] = self.batch_id

        return i

    def closed(self, reason):

        url = '{}/api/crawl_schedule/{}/'.format(os.getenv('DJANGO_HOST'), self.scheduled_crawl_id)
        payload = {
            'id': self.scheduled_crawl_id,
            'status': 'Done'
        }

        try:
            r = requests.put(url, json=payload)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logging.error(r.text)

        # close the connection to rabbitmq
        self.rmq.close()

