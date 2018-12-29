#!/usr/bin/env python2
# -*- encoding=utf-8 -*-
import scrapy
from ..items import CigaretteItem


class CigaretteSpider(scrapy.Spider):
    name = "cigarette-xpath"
    allowed_domins = "cnxiangyan.com"

    start_urls = {
        'https://www.cnxiangyan.com/brand/'
    }

    def parse(self, response):
        for cigarette in response.xpath('//div[@class="prodlist"]/ul[@class="list"]/li'):

            name = cigarette.xpath('.//div[@class="name"]/h2/text()').extract_first();

            if name is None:
                name = cigarette.xpath('.//div[@class="name"]/h2/b/text()').extract_first();

            item = CigaretteItem()
            item['name'] = name
            item['category'] = cigarette.xpath('.//div[@class="type"]/p/text()').extract()
            item['tarContent'] = cigarette.xpath('.//div[@class="tar"]/p/text()').extract()
            item['price'] = cigarette.xpath('.//div[@class="price"]/p/text()').extract()
            item['img'] = cigarette.xpath('.//div[@class="img"]/img/@src').extract_first()
            yield item

        next_page_url = response.xpath(u'//a[contains(text(),"下一页")]/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
