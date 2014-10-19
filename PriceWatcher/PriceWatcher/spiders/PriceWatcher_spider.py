import scrapy
from PriceWatcher.items import PriceWatcherItem
from PriceWatcher.SitesAndURLs import *

class PriceWatcherSpider(scrapy.spider):
    name = "PriceWatcher"
    allowed_domain = URL_SAKS

    start_urls = URL_SALE_BAG_SAKS

    def parse(self, response):
        pass