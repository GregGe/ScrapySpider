# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class GiftCategoryItem(scrapy.Item):
    category = scrapy.Field()
    sub_category = scrapy.Field()
    tag = scrapy.Field()
    tag_url = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()
    like_num = scrapy.Field()
    price = scrapy.Field()
    detail = scrapy.Field()
    img_url = scrapy.Field()
    img_path = scrapy.Field()

class GiftItem(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    like_num = scrapy.Field()
    price = scrapy.Field()
    detail = scrapy.Field()
    img_url = scrapy.Field()
    img_path = scrapy.Field()