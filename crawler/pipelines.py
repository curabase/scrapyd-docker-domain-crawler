# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import requests
import json
import uuid
import logging

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
            'categories': item['categories'],
            'batch_id': item['batch_id']
        }])

        if spider.settings.get('SOLR_HOST'):
            url = 'http://{}:8983/solr/defaultcore/update?commit=true'.format(spider.settings.get('SOLR_HOST'))

            try:
                r = requests.post(url, headers=headers, data=data)
                r.raise_for_status()
            except requests.exceptions.HTTPError as e:
                logging.error(r.text)

        return item


class PushToDjangoPipeline(object):
    def process_item(self, item, spider):

        headers = {
            'Content-Type': 'application/json'
        }

        id = str(uuid.uuid5(uuid.NAMESPACE_URL, item['url']))
        data = json.dumps({
            'id' : id,
            'url' : item['url'],
            'domain' : item['domain'],
            'h1': item['h1'],
            'h2': item['h2'],
            'body': item['body'],
            'description': item['description'],
            'title': item['title'],
            'categories': item['categories'],
            'batch_id': item['batch_id']
        })

        url = 'http://django:8000/api/page/'

        try:
            logging.debug(data)
            r = requests.post(url, headers=headers, data=data)
            r.raise_for_status()
        except requests.exceptions.HTTPError as e:
            logging.error(r.text)

        return item
