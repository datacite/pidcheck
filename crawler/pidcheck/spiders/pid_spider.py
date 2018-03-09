import scrapy
import json
from scrapy_redis.spiders import RedisSpider
from scrapy_redis.utils import bytes_to_str

from datetime import datetime
from extruct.jsonld import JsonLdExtractor
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError, ConnectError
from pidcheck.items import PidCheckResult

class PidMixin():
    handle_httpstatus_list = [404] # Tell scrapy to not ignore these codes

    def parse(self, response):
        pid_check = PidCheckResult()

        pid_check['pid'] = response.meta['pid']
        pid_check['checked_url'] = response.url
        pid_check['checked_date'] = datetime.now()
        pid_check['error'] = ''

        # Store extra HTTP data from the response
        pid_check['redirect_count'] = response.meta.get('redirect_times', 0)
        pid_check['redirect_urls'] = response.meta.get('redirect_urls', [])
        pid_check['download_latency'] = response.meta.get('download_latency', 0) * 1000 # Ms

        # Store http status
        pid_check['http_status'] = response.status

        # Only do body extraction if we got something in the body
        if response.body:
            # Extract schema.org json ld
            extractor = JsonLdExtractor()
            schema_org = extractor.extract(response.body, response.url)

            pid_check['schema_org_id'] = None
            pid_check['schema_org'] = None
            if schema_org:
                # Technically there can be multiple schema_org json LD sections,
                # but in practice there will likely only be one that makes sense.
                # So pick the first out of the list as our schema
                pid_check['schema_org'] = schema_org[0]

                # The schema has two distinct definitions for identifiers,
                # @id seems to be for usecases where it is a URI only,
                # however some still suggest using 'identifier'
                pid_check['schema_org_id'] = pid_check['schema_org'].get('@id')
                if not pid_check['schema_org_id']:
                    pid_check['schema_org_id'] = pid_check['schema_org'].get('identifier')

            # Extract all identifiers listed with dublin core syntax.
            pid_check['dc_identifier'] = response.xpath("//meta[@name='DC.identifier']/@content").extract_first()

            # Extract citation_doi metadata
            pid_check['citation_doi'] = response.xpath("//meta[@name='citation_doi']/@content").extract_first()

            # Try looking for the pid in the body
            pid_text = response.xpath("//*[contains(text(), '{0}')]".format(pid_check['pid'])).extract_first()
            pid_check['body_has_pid'] = pid_text != None

        yield pid_check

    def handle_errors(self, failure):
        pid_check = PidCheckResult()

        request = failure.request

        pid_check['pid'] = request.meta['pid']
        pid_check['checked_url'] = request.url
        pid_check['error'] = ''

        if failure.check(HttpError):
            response = failure.value.response
            pid_check['http_status'] = response.status
            pid_check['error'] = "HTTP Error"
        elif failure.check(DNSLookupError):
            self.logger.error('DNSLookupError on %s', request.url)
            pid_check['error'] = "DNS lookup failure"

        elif failure.check(TimeoutError, TCPTimedOutError, ConnectError):
            pid_check['error'] = "Timeout"
            self.logger.error('TimeoutError on %s', request.url)

        yield pid_check


class PidSpider(PidMixin, RedisSpider):
    name = "pidcheck"

    def make_request_from_data(self, data):
        url = json.loads(bytes_to_str(data, self.redis_encoding))
        request = scrapy.Request(url=url['url'], callback=self.parse, errback=self.handle_errors)
        request.meta['pid'] = url['pid']
        return request