# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import requests
import json


class DomainGrabberPipeline(object):
    def process_item(self, item, spider):
        return item

class PushToSolrPipeline(object):
    def process_item(self, item, spider):
        headers = {
            'Content-Type': 'application/json'
        }

        data = json.dumps([{
            'url' : item['url'],
            'domain' : item['domain'],
            'h1': item['h1'],
            'h2': item['h2'],
            'body': item['body'],
            'description': item['description'],
            'title': item['title'],
            'category': item['category']
        }])

        solr_url = 'http://{}:8983/solr/defaultcore/update?commit=true'.format(spider.settings.get('SOLR_HOST','solr'))
        r = requests.post(solr_url, headers=headers, data=data)

        return item
