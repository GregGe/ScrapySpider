#!/usr/bin/env python2
# -*- encoding=utf-8 -*-

import scrapy

from ..items import CoupletItem
from ..items import NumberCoupletItem
from ..items import ZodiacCoupletItem


class CoupletSpieder(scrapy.Spider):
    DEBUG = True
    name = "topscroll-xpath"
    allowed_domins = "duiduilian.com"

    start_urls = {
        'http://www.duiduilian.com/chunlian/hengpi.html'
    }

    host = 'http://www.duiduilian.com/chunlian/hengpi.html'

    def parse(self, response):
        url_prefix = self.host[:-5]

        urls = []
        nums = []

        page_xpath = response.xpath("//div[@id='pages']/a")
        for page in page_xpath:
            try:
                num = int(page.xpath("./text()").extract_first())
                nums.append(num)
            except Exception as e:
                # print(e)
                pass
        max_page = max(nums)
        urls.append(self.host)
        for index in range(1, max_page + 1):
            next_url = url_prefix + ("_%s.html" % index)
            urls.append(next_url)

        for url in urls:
            yield scrapy.Request(url=url, dont_filter=True, callback=self.parse_content)

    def parse_content(self, response):
        item = CoupletItem()
        p_style_xpath = response.xpath("//div[@class='content_zw']//p")
        for couplet_xpath in p_style_xpath:
            part = couplet_xpath.xpath("./text()").extract_first()
            item['top_scroll'] = part.strip()
            yield item
