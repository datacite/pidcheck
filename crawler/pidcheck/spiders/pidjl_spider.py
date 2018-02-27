import scrapy
import json
from .pid_mixin import PidMixin

class PidJLSpider(PidMixin, scrapy.Spider):
    name = "pidcheck-jl"
    url_file = 'urls.jl'

    custom_settings = {
        'SCHEDULER': 'scrapy.core.scheduler.Scheduler',
        'ITEM_PIPELINES': {'pidcheck.pipelines.PIDMetadataIDPipeline': 300},
        'DUPEFILTER_CLASS': 'scrapy.dupefilters.RFPDupeFilter',
    }

    def start_requests(self):
        with open(self.url_file) as f:
            for jl in f:
                url = json.loads(jl)
                request = scrapy.Request(url=url['url'], callback=self.parse)
                request.meta['pid'] = url['pid']
                yield request