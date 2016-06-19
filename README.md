Required command line params for the `domain_spider` crawler

    `scrapy crawl domain_spider -a url=https://www.3cosystem.com -s FEED_URI=${FEED_URI}3cosystem.com/3co.jsonl`

Before running `worker.py` you will want to set the following environment variables:

    `FEED_URI` : 


Crawler options:

  - allowed
  - denied
  - 

using `-s FEED_URI_=` will tell the spider to upload the scraped data (in jsonlines format) to a filehost of your choice. In
this case, we also use azure's Blob storage.

the format for that url is: `azure://account_name_:password@container/`

