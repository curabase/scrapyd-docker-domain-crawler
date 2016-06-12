import os
import time

if __name__ == '__main__':

    ES_SERVER=os.getenv('ES_SERVER')
    ES_INDEX=os.getenv('ES_INDEX')

    while True:
        # todo: poll from redis

        # 
        os.system('scrapy crawl domain_spider -a es_server={} -a es_index={} -a url={}'.format(ES_SERVER, ES_INDEX, url)

    print('called here')
