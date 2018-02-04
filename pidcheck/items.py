# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class PIDCheck(scrapy.Item):
    request_url = scrapy.Field()
    response_url = scrapy.Field()
    redirect_count = scrapy.Field()
    redirect_urls = scrapy.Field()
    download_latency = scrapy.Field()
    checked_date = scrapy.Field()
    problems = scrapy.Field()
    schema = scrapy.Field()