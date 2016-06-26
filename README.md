# Purpose

This is a "dockerized" scrapyd instance with a custom spider automatically  
deployed. It is meant to be a general purpose web scraper that can output 
its raw crawl data file locally or to an Azure blob storage account.
 
 
# Item format

The scrapy item looks like this:

 - domain
 - title
 - description
 - body
 - h1
 - h2
 - url
 - category
 
# Spider params
 
 The spider takes custom parameters upon initialization. These are passed 
 directly to the crawler class.
 
  - `url`: the full web address of the site to crawl (eg - https://www.djangoprojec.com)
  - `allowed`: a regex string which tells the spider which URLs are valid to 
 crawl (see http://doc.scrapy.org/en/latest/topics/link-extractors.html#module-scrapy.linkextractors.lxmlhtml)
  - `denied`: a regex string which tells the spider which URLs are denied 
 (see http://doc.scrapy.org/en/latest/topics/link-extractors.html#module-scrapy.linkextractors.lxmlhtml)
  - `single_page`: a boolean which tells the spider to crawl only the given url
 
# Overriding settings.py

  - `FEED_URI`: will tell the spider to upload the scraped data (in jsonlines format) to a filehost of your choice. In
this case, we also use azure's Blob storage. The format for that url is: `azure://account_name_:password@container/path1/path2/filename.jsonl`
  - `DEPTH_LIMIT`: The maximum depth that will be allowed to crawl for any site. If zero, no limit will be imposed. (http://doc.scrapy.org/en/latest/topics/settings.html#depth-limit)

**NOTE**: If `FEED_URI` is left unset, then your spider will not save its output to a file. Your only ouput will be from
your item_pipelines.


# Deploy the spider to scrapyd
If you want to "eggify" the project, simply run this command:

`python setup.py clean -a bdist_egg -d <output_folder>`

This will do all that is necessary to deploy your spider to scrapyd. You may have to edit scrapy.cfg.

Note, the preferred method is to use a `build.sh` script. (See below).


# Deploy the spider to your own docker private registry

There is a file called `build.sh.sample` that will quickly tag and push a new image to your registry.
Simply rename the file to build.sh and edit the tag names and host to which you want to push.


# Running the spider with docker

This is the preferred method. It will build the docker image and deploy the spider to a running scrapyd instance. You
can then schedule jobs using the HTTP API on the docker images IP address.

**NOTE**: if using curl, you will need to replace `+` chars wtih `%2B`, otherwise it 
gets eaten and turned into a ` ` (space).

Calling from the command line:

`curl -XPOST http://localhost:6800/schedule.json -d  project=crawler -d spider=domain_spider -d url=http://www.m3b.net -d setting=FEED_URI='azure://accountname:queXX59YrwTbm1KUj0lK1gXHv4NHrCfKxfxHy3bwQJ%2BLqFHCay6r1S/Yhw2Ot4Tk6p1zFakfjdaskfjnaksZgA==@sites/m3b.net/hahaha123000.jsonl'`


# Running the spider without scrapyd

Required command line params for the `domain_spider` crawler

    `scrapy crawl domain_spider -a url=https://www.3cosystem.com -s FEED_URI=${FEED_URI}3cosystem.com/3co.jsonl`


# Developing this codebase

You will want to `pip install -r requirements/development.txt` so that you can edit the Azure blob storage codebase in 
tandem with this repo (if necessary).


# License

I don't know yet, but most likely MIT license.