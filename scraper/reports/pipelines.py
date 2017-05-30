# -*- coding: utf-8 -*-

import pymongo

from scrapy.conf import settings
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from scrapy.exceptions import DropItem
from dragnet import content_extractor



class ContentExtractor(object):


    def process_item(self, item, spider):
        fullHTML = item['content']
        content = content_extractor.analyze(fullHTML)
        item['content'] = content

        return item






class MongoConnector(object):

    def __init__(self):
        self.connection = MongoClient(
            settings['MONGODB_SERVER'],
            settings['MONGODB_PORT']
        )
        self.db = self.connection[settings['MONGODB_DB']]
        self.collection = self.db[settings['MONGODB_COLLECTION']]
    

    def process_item(self, item, spider):
        valid = True

        if not item['url']:
            valid = False
            raise DropItem("Missing url!")

        if not item['company']:
            valid = False
            raise DropItem("Missing company!")

        if valid:
            try:
                self.collection.insert(dict(item))
            except (DuplicateKeyError):
                raise DropItem("Duplicate {0}!".format(item['url']))

        return item

    def close_spider(self, spider):
        self.connection.close()

