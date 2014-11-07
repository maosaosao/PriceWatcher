import random
import time
from twisted.internet import reactor
from scrapy.crawler import Crawler
from scrapy import log, signals
from PriceWatcher.spiders.PriceWatcher_spider import PriceWatcherSpider
from scrapy.utils.project import get_project_settings

log.start()

spider = PriceWatcherSpider(domain='barneys.com')
settings = get_project_settings()
crawler = Crawler(settings)
crawler.signals.connect(reactor.stop, signal=signals.spider_closed)
crawler.configure()
crawler.crawl(spider)
crawler.start()
reactor.run()
