from __future__ import absolute_import, print_function

import scrapy

from ..items import SurfTVItem

class TVTSpider(scrapy.Spider):
    name = 'tvt'
    allowed_domains = ['tvtropes.org']

    start_urls = [
        'http://tvtropes.org/pmwiki/pmwiki.php/Main/Tropes',
    ]

    url_root = 'http://tvtropes.org/pmwiki/pmwiki.php/'

    def parse(self, response):
        if not response.url.startswith(self.url_root):
            # probably a redirection to a non-wiki page that originally looked like one
            return

        item = SurfTVItem()
        item['url'] = response.url[len(self.url_root):]

        title = response.xpath('/html/head/title/text()').extract()
        item['title'] = title[0] if title else ''

        article_body = response.css('.main')
        item['body'] = ''.join(article_body.extract())

        item['outlinks'] = (article_body
            .xpath('/descendant::a[@class="twikilink"]/@href')
            .re('pmwiki\.php/(.*)')
        )
        yield item

        for n, outlink in enumerate(item['outlinks']):
            yield scrapy.Request(self.url_root + outlink)
            # if n >= 10:
            #     break
