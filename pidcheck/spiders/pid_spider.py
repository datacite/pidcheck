import scrapy
from datetime import datetime
from extruct.jsonld import JsonLdExtractor
from pidcheck.items import PIDCheck

class PidSpider(scrapy.Spider):
    name = "pid"
    handle_httpstatus_list = [404, 500] # Tell scrapy to not ignore these codes

    def start_requests(self):
        urls = [
            'https://doi.org/10.5438/msk0-7250',
            'https://doi.org/10.5438/ea4h-tx3g'
        ]

        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        pid_check = PIDCheck()

        pid_check['url'] = response.url
        pid_check['checked_date'] = datetime.now()

        problems = []

        # Handle if we have a DOI(pid?) in the URL, extract it, does it match what the metadata tells us

        # Check HTTP Status codes for possible problems
        problems += self.check_http_status(response.status)

        # Extract Schema.org json ld
        extractor = JsonLdExtractor()
        schema = extractor.extract(response.body_as_unicode(), response.url)
        pid_check['schema'] = schema

        # Check schema
        problems += self.check_schema(schema)

        # Add details to the link result
        pid_check['problems'] = problems

        self.log('hit %s' % response.url)
        yield pid_check

    def check_http_status(self, status):
        problems = []

        # Check for regular 404
        if status == 404:
            problems.append("Http 404, not found")

        return problems

    def check_schema(self, schema):
        problems = []

        if schema:
            # Look for a PID ID
            pid = schema[0].get('@id')

            if not pid:
                problems.append("PID Missing in JsonLD schema.org metadata")
        else:
            problems.append("Missing embedded schema.org metadata")

        return problems