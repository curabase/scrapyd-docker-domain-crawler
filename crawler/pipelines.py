# -*- coding: utf-8 -*-
import json
import pika


class PushToRabbitMQPipeline(object):

    def process_item(self, item, spider):

        data = json.dumps({
            'url': item['url'],
            'domain': item['domain'],
            'h1': item['h1'],
            'h2': item['h2'],
            'body': item['body'],
            'description': item['description'],
            'title': item['title'],
            'categories': item['categories'],
            'batch_id': item['batch_id']
        })

        spider.channel.basic_publish(
            exchange='',
            routing_key='page_publish',
            body=data,
            properties=pika.BasicProperties(delivery_mode=2,)
        )
