import scrapy
import json
from scrapy_redis.spiders import RedisSpider
from scrapy_redis.utils import bytes_to_str
from pid_mixin import PidMixin

class PidSpider(PidMixin, RedisSpider):
    name = "pidcheck"

    def make_request_from_data(self, data):
        url = json.loads(bytes_to_str(data, self.redis_encoding))
        request = scrapy.Request(url=url['url'], callback=self.parse)
        request.meta['pid'] = url['pid']
        return request