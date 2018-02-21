# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class PIDCheck(scrapy.Item):
    pid = scrapy.Field()
    checked_url = scrapy.Field()
    redirect_count = scrapy.Field()
    redirect_urls = scrapy.Field()
    download_latency = scrapy.Field()
    checked_date = scrapy.Field()
    schema_org = scrapy.Field()
    schema_org_id = scrapy.Field()
    dc_identifier = scrapy.Field()
    citation_doi = scrapy.Field()
    http_status = scrapy.Field()
    pid_meta_match = scrapy.Field()
    pid_meta_different = scrapy.Field()
    body_has_pid = scrapy.Field()

    problems = scrapy.Field()