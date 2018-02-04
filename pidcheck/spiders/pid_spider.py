import scrapy
import json
from datetime import datetime
from extruct.jsonld import JsonLdExtractor
from pidcheck.items import PIDCheck

class PidSpider(scrapy.Spider):
    name = "pid"
    url_file = 'urls.jl'
    handle_httpstatus_list = [404, 500] # Tell scrapy to not ignore these codes

    def start_requests(self):

        with open(self.url_file) as f:
            for jl in f:
                url = json.loads(jl)
                request = scrapy.Request(url=url['url'], callback=self.parse)
                request.meta['pid'] = url['pid']
                yield request

    def parse(self, response):
        pid_check = PIDCheck()

        pid_check['pid'] = response.meta['pid']
        pid_check['checked_url'] = response.url
        pid_check['checked_date'] = datetime.now()

        # Store extra HTTP data from the response
        pid_check['redirect_count'] = response.meta.get('redirect_times', 0)
        pid_check['redirect_urls'] = response.meta.get('redirect_urls', [])
        pid_check['download_latency'] = response.meta.get('download_latency', 0) * 1000 # Ms

        # Store http status
        pid_check['http_status'] = response.status

        # Extract schema.org json ld
        extractor = JsonLdExtractor()
        schema_org = extractor.extract(response.body, response.url)
        pid_check['schema_org'] = schema_org

        # Extract all identifiers listed with dublin core syntax.
        pid_check['dc_identifiers'] = response.xpath("//meta[@name='DC.identifier']/@content").extract()

        self.log('hit %s' % response.url)
        yield pid_check
