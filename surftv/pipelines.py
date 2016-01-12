# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html

# stdlib
import re

# third party
import pymongo


class SurfTVPipeline(object):

    collection_name = 'tvt_items'

    title_pattern = re.compile(r'''
        ^
        (?P<title>[\w ]+)\ (
            (
                \/\ (?P<ns1>[\w ]+)
                |
                \((?P<ns2>[\w ]+)\)
            )
        \ )?
        -\ TV\ Tropes
        $
    ''', flags=re.VERBOSE)

    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGO_URI', 'mongodb://localhost:27017/'),
            mongo_db=crawler.settings.get('MONGO_DATABASE', 'scrapy')
        )

    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        doc = dict(item)
        doc['success'] = False

        match = self.title_pattern.match(doc['title'])
        if match:
            doc['success'] = True
            md = match.groupdict()
            # http://stackoverflow.com/a/2364277/194586
            doc['namespace'] = next((x for x in [md['ns1'], md['ns2']] if x), 'Main')
            doc['title'] = md['title']

        self.db[self.collection_name].insert(doc)
        return item
