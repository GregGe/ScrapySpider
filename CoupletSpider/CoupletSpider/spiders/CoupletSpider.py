#!/usr/bin/env python2
# -*- encoding=utf-8 -*-

import scrapy
import logging

from ..items import CoupletItem
from ..items import NumberCoupletItem
from ..items import ZodiacCoupletItem


class CoupletSpieder(scrapy.Spider):
    DEBUG = False
    name = "couplet-xpath"
    allowed_domins = "duiduilian.com"

    start_urls = {
        'http://www.duiduilian.com/chunlian/'
    }

    host = 'http://www.duiduilian.com/'

    def parse(self, response):
        category = response.xpath("//div[@class='content_list']//div[@class='pd_list_3 l5 l_dot']//ul")
        items = []

        for zodiac_response in category[0].xpath("./li"):
            name = zodiac_response.xpath('./a/text()').extract_first()

            if (u'年春联' in name):
                name = name.replace(u'年春联', '')

            zodiac_item = ZodiacCoupletItem()
            zodiac_item['name'] = name
            zodiac_item['url'] = self.host + zodiac_response.xpath('./a/@href').extract_first()

            items.append(zodiac_item)

        for num_response in category[1].xpath("./li"):
            name = num_response.xpath('./a/text()').extract_first()
            if (u'字' in name):
                name = name.replace(u'字', '')
            num_item = NumberCoupletItem()
            num_item['name'] = name
            num_item['url'] = self.host + num_response.xpath('./a/@href').extract_first()

            items.append(num_item)

        if self.DEBUG:
            debug_url = 'http://www.duiduilian.com//chunlian/7zi.html'
            debug_name = '7'
            yield scrapy.Request(url=debug_url, meta={
                "item": {'name': debug_name, 'url': debug_url}}, callback=self.parse_pages)
        else:
            for item in items:
                yield scrapy.Request(url=item['url'], meta={"item": item}, dont_filter=True,
                                     callback=self.parse_pages)

    def parse_pages(self, response):
        category_item = response.meta['item']
        url = category_item['url']
        is_five_num = (u'5' == category_item['name'])
        url_prefix = url[:-5]

        urls = []
        nums = []

        page_xpath = response.xpath("//div[@id='pages']/a")
        if page_xpath:
            for page in page_xpath:
                try:
                    num = int(page.xpath("./text()").extract_first())
                    nums.append(num)
                except Exception as e:
                    # print(e)
                    pass
            max_page = max(nums)
            urls.append(url)
            for index in range(2, max_page + 1):
                next_url = url_prefix + ("_%s.html" % index)
                urls.append(next_url)
        else:
            page_table_xpath = response.xpath("//tbody//tr//td//a")
            if page_table_xpath:
                for page in page_table_xpath:
                    next_url = page.xpath("./@href").extract_first()
                    if next_url:
                        url = self.host + next_url
                        if is_five_num:
                            url = url.replace(u'chunjie', u"chunlian")
                        urls.append(url)
            else:
                urls.append(url)

        if self.DEBUG:
            for url in urls:
                print(url)

        for url in urls:
            yield scrapy.Request(url=url, meta={"item": category_item}, dont_filter=True, callback=self.parse_content)

    def parse_content(self, response):
        category_item = response.meta['item']

        item = CoupletItem()
        item['category'] = category_item['name']
        is_four_num_style = (u'4' == item['category'])
        is_five_num_style = (u'5' == item['category'])
        is_seven_num_style = (u'7' == item['category'])
        p_style_xpath = response.xpath("//div[@class='content_zw']//p")
        if p_style_xpath:
            for couplet_xpath in p_style_xpath:
                if is_four_num_style:
                    part = couplet_xpath.xpath("./text()").extract_first().strip().split(u"，")
                    item['up_part'] = part[0]
                    if part[1].__len__() > 4:
                        texts = part[1].split(u"（")
                        item['down_part'] = texts[0]
                        item['desc'] = texts[1].replace(u"）", "").strip()
                    else:
                        item['down_part'] = part[1]
                        item['desc'] = ''
                    item['top_scroll'] = ''
                elif is_five_num_style:
                    part = couplet_xpath.xpath("./font/text()").extract()
                    part = filter(lambda str: str.strip(), part)
                    if part.__len__() >= 1:
                        text = part[0].strip()
                        if text.__len__() > 10:
                            texts = text.split(u"，")
                            item['up_part'] = texts[0]
                            item['down_part'] = texts[1]
                            if part.__len__() > 1:
                                item['desc'] = part[1]
                            else:
                                item['desc'] = ''
                        elif part.__len__() == 2:
                            item['up_part'] = part[0]
                            item['down_part'] = part[1]
                            item['desc'] = ''
                        else:
                            current_url = response._get_url()
                            self.log('Parse the couplet error! Url = ' + current_url, logging.ERROR)
                        item['top_scroll'] = ''
                    else:
                        current_url = response._get_url()
                        self.log('Parse the couplet error! Url = ' + current_url, logging.ERROR)
                        continue

                elif is_seven_num_style:
                    part = couplet_xpath.xpath("./font/text()").extract()
                    if part.__len__() >= 2:
                        item['up_part'] = part[0].replace(u"）", "").strip()
                        item['down_part'] = part[1].replace(u"）", "").strip()
                        if part.__len__() > 2:
                            item['desc'] = part[2].replace(u"）", "").strip()
                        else:
                            item['desc'] = ''

                else:
                    desc = couplet_xpath.xpath("./font/text()").extract_first()
                    if desc:
                        desc = desc.strip().replace(u"（", "").replace(u"）", "")
                        if u'横批' in desc:
                            item['top_scroll'] = desc.replace(u"横批：", "")
                            item['desc'] = ''
                        else:
                            item['desc'] = desc
                            item['top_scroll'] = ''
                    else:
                        item['top_scroll'] = ''
                        item['desc'] = ''
                    part = couplet_xpath.xpath("./text()").extract()
                    part = filter(lambda str: str.strip(), part)
                    len = part.__len__()
                    if len <= 0:
                        continue
                    elif len == 1:
                        part = part[0].split(u'；')
                        part = filter(lambda str: str.strip(), part)
                        if part.__len__() >= 2:
                            item['up_part'] = part[0].strip().replace("\"", "").replace(u"；", "")
                            item['down_part'] = part[1].strip().replace("\"", "").replace(u"。", "")
                        else:
                            current_url = response._get_url()
                            self.log('Parse the couplet error! Url = ' + current_url, logging.ERROR)
                            continue
                    elif len == 2:
                        item['up_part'] = part[0].strip().replace("\"", "").replace(u"；", "")
                        item['down_part'] = part[1].strip().replace("\"", "").replace(u"。", "")
                    elif len == 3:
                        item['up_part'] = part[0].strip().replace("\"", "").replace(u"；", "")
                        item['down_part'] = part[1].strip().replace("\"", "").replace(u"。", "")
                        item['top_scroll'] = part[2].strip().replace(u"横批：", "")
                    else:
                        current_url = response._get_url()
                        self.log('Parse the couplet error! Url = ' + current_url, logging.ERROR)
                        continue

                yield item
        else:
            parts = []
            try:
                num = int(item['category'])
            except:
                # zodiac
                num = -1
            for item_str in response.xpath("//div[@class='content_zw']/text()").extract():
                item_str = item_str.strip().replace('\r\n', '')
                if item_str.__len__() > 0 and item_str.__len__() >= num:
                    parts.append(item_str)
            for i in range(0, parts.__len__(), 2):
                item['down_part'] = parts[i + 1]
                if parts[i].__len__() == parts[i + 1].__len__():
                    item['up_part'] = parts[i]
                    item['top_scroll'] = ''
                    item['desc'] = ''
                else:
                    strs = parts[i].split(" ")
                    strs = filter(lambda str: str.strip(), strs)
                    item['up_part'] = strs[0]
                    desc = strs[1]
                    if u'横批' in desc:
                        item['top_scroll'] = desc.replace(u"横批：", "")
                        item['desc'] = ''
                    else:
                        item['desc'] = desc
                        item['top_scroll'] = ''
                yield item
