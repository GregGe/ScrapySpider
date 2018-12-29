#!/usr/bin/env python2
# -*- encoding=utf-8 -*-

import scrapy
from ..items import GiftItem


class GiftSpieder(scrapy.Spider):
    name = "christmas-gift-xpath"
    allowed_domins = "cocodiy.com"

    host_url = "http://www.cocodiy.com"

    start_urls = {
        'http://www.cocodiy.com/topic/121'
    }

    def parse(self, response):
        for gift in response.xpath("//div[@class='index-probox clearfix']//ul[@class='clearfix']/li"):
            item = GiftItem()
            item['id'] = gift.xpath("./@id").extract_first()
            name = gift.xpath(".//dd[@class='name']/a/text()").extract_first()
            item['name'] = name.encode(encoding='UTF-8', errors='strict')
            item['like_num'] = gift.xpath(".//a[@class='likebut']/@rel").extract_first()
            item['price'] = gift.xpath(".//span[@class='m-num']/text()").extract_first()
            item['img_url'] = [gift.xpath(".//a[@class='img-h']//img[@class='lazy']/@data-original").extract_first()]
            item['detail'] = ""
            items_url = self.host_url + gift.xpath(".//a[@class='img-h']/@href").extract_first()
            yield scrapy.Request(url=items_url, meta={"item": item}, callback=self.parse_detail)

    def parse_detail(selfs, response):
        item = response.meta['item']
        detail = response.xpath("//div[@class='pro_tips']/text()").extract_first()
        print(response.body)
        print(detail)
        item['detail'] = detail  # detail.encode(encoding='UTF-8', errors='strict')
        yield item
