Required command line params for the `domain_spider` crawler

  `scrapy crawl domain_spider -a url=<url> -s ELASTICSEARCH_SERVER=<http://HOSTNAME:port> -s ELASTICSEARCH_INDEX=<index_name>`

Before running `worker.py` you will want to set the following environment variables:

  * `ELASTICSEARCH_SERVER='http://<hostname>:port'`  # hostname and port of the elasticsearch server
  * `ELASTICSEARCH_INDEX=index_name # the index in the database where the results will go

