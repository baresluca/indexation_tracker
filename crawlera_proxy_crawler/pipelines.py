# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import re

class CrawleraProxyCrawlerPipeline(object):
    def process_item(self, item, spider):
        regex = '^https\S*q=\%22(\S*)\%22$'
        regex_result = re.match(regex, item['scraped_url'])
        item['vistaprint_url'] = regex_result.group(1)
        
        if item['no_match']:
            item['indexed_url'] = "Not Indexed"
        elif not item['links']:
            item['indexed_url'] = "Not Indexed"
        else:   
            for link in item['links']:
                if item['vistaprint_url'] == link:
                    item['indexed_url'] = "Indexed"
                    break
                else:
                    item['indexed_url'] = "Not Indexed" 
        return item
