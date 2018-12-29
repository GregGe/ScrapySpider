# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class CoupletItem(scrapy.Item):
    # 上联
    up_part = scrapy.Field()
    # 下联
    down_part = scrapy.Field()
    # 横批
    top_scroll = scrapy.Field()
    # 分类
    category = scrapy.Field()
    # 描述
    desc = scrapy.Field()


class ZodiacCoupletItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()


class NumberCoupletItem(scrapy.Item):
    name = scrapy.Field()
    url = scrapy.Field()
