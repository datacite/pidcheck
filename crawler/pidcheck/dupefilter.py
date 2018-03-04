from scrapy_redis.dupefilter import RFPDupeFilter

class PidDupeFilter(RFPDupeFilter):
    def request_seen(self, request):
        return False
