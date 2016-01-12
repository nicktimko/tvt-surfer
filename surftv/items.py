# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class SurfTVItem(scrapy.Item):
    namespace = scrapy.Field()
    title = scrapy.Field()
    url = scrapy.Field()
    body = scrapy.Field()
    outlinks = scrapy.Field()

    def __repr__(self):
        return "<SurfTVItem '{}':'{}', {} outlinks, {:,} B body>".format(
            self.get('namespace', '<none>'),
            self.get('title', '<none>'),
            len(self.get('outlinks', '')),
            len(self.get('body', ''))
        )
