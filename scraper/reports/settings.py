# -*- coding: utf-8 -*-

BOT_NAME = 'reports'

SPIDER_MODULES = ['reports.spiders']
NEWSPIDER_MODULE = 'reports.spiders'


# Crawl responsibly by identifying yourself (and your website) on the user-agent
USER_AGENT = 'SustainabilityBot http://goo.gl/4VlxkT'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True


# Crawl in BFO order
DEPTH_PRIORITY = 1
SCHEDULER_DISK_QUEUE = 'scrapy.squeues.PickleFifoDiskQueue'
SCHEDULER_MEMORY_QUEUE = 'scrapy.squeues.FifoMemoryQueue'

# Configure a delay for requests for the same website (default: 0)
DOWNLOAD_DELAY = 5
DEPTH_LIMIT = 3


# Override the default request headers:
DEFAULT_REQUEST_HEADERS = {
  'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
  'Accept-Language': 'en',
}


REDIRECT_MAX_TIMES = 3



# Configure item pipelines
ITEM_PIPELINES = {
    'reports.pipelines.ContentExtractor': 300,
    'reports.pipelines.MongoConnector': 800,
}

MONGODB_SERVER = "localhost"
MONGODB_PORT = 27017
MONGODB_DB = "sustainability"
MONGODB_COLLECTION = "webpages"

