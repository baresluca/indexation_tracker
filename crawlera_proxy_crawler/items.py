# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CrawleraProxyCrawlerItem(scrapy.Item):
    scraped_url = scrapy.Field()
    vistaprint_url = scrapy.Field()
    links = scrapy.Field()
    no_match = scrapy.Field()
    indexed_url = scrapy.Field()
    status_code = scrapy.Field()
    error_code = scrapy.Field()

