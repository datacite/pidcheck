import scrapy
from datetime import datetime
from extruct.jsonld import JsonLdExtractor

class PidSpider(scrapy.Spider):
    name = "pid"
    handle_httpstatus_list = [404, 500] # Tell scrapy to not ignore these codes

    start_urls = (
        'https://doi.org/10.5438/msk0-7250',
        'https://doi.org/10.5438/ea4h-tx3g'
    )

    def parse(self, response):
        yield {}