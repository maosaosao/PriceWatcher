# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class PriceWatcherItem(scrapy.Item):
    # define the fields for your item here like:
    id=scrapy.Field()
    name=scrapy.Field()
    price=scrapy.Field()
    originalPrice=scrapy.Field()
    designer=scrapy.Field()
    link=scrapy.Field()
