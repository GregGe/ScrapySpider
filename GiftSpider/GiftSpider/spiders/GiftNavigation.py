import scrapy
from ..items import GiftItem
from ..items import GiftCategoryItem


class GiftSpieder(scrapy.Spider):
    name = "christmas-giftnav-xpath"
    allowed_domins = "cocodiy.com"

    host_url = "http://www.cocodiy.com"

    start_urls = {
        'http://www.cocodiy.com/topic/'
    }

    def parse(self, response):
        categorys = list()
        for i in range(1, 4):
            category_name = response.xpath("//div[@class='liwu_nav_title c%s mb']/h2/text()" % i).extract_first()
            # three box
            for index in range(1, 4):
                sub_category = response.xpath(
                    "//div[@class='liwu_box c%s mb20']//li[%s]//div[1]//div[1]/h2/text()" % (i, index)).extract_first()
                for item in response.xpath(
                        "//div[@class='liwu_box c%s mb20']//ul[@class='clearfix']//li[%s]//div[1]//div[2]/a" % (
                                i, index)):
                    tag = item.xpath("./span/text()").extract_first()
                    tag_url = self.host_url + item.xpath("./@href").extract_first()
                    category = GiftCategoryItem()
                    category['category'] = category_name
                    category['sub_category'] = sub_category
                    category['tag'] = tag
                    category['tag_url'] = tag_url
                    categorys.append(category)

        category_name = response.xpath("//div[@class='liwu_nav_title c4 mb']/h2/text()").extract_first()
        for i in range(1, 4):
            sub_category = response.xpath(
                "//div[@class='liwu_box c4']//ul[@class='clearfix']//li[%s]//div[1]//div[1]/h2/text()" % i).extract_first()
            for item in response.xpath(
                    "//div[@class='liwu_box c4']//ul[@class='clearfix']//li[%s]//div[1]//div[2]/a" % i):
                tag = item.xpath("./span/text()").extract_first()
                tag_url = self.host_url + item.xpath("./@href").extract_first()
                category = GiftCategoryItem()
                category['category'] = category_name
                category['sub_category'] = sub_category
                category['tag'] = tag
                category['tag_url'] = tag_url
                categorys.append(category)

        # return categorys
        for category in categorys:
            yield scrapy.Request(url=category['tag_url'], meta={"category": category}, callback=self.parse_item)

    def parse_item(self, response):
        category = response.meta['category']
        for gift in response.xpath("//div[@class='index-probox clearfix']//ul[@class='clearfix']/li"):
            item = GiftCategoryItem()
            item['category'] = category['category']
            item['sub_category'] = category['sub_category']
            item['tag'] = category['tag']
            item['tag_url'] = category['tag_url']

            item['id'] = gift.xpath("./@id").extract_first()
            name = gift.xpath(".//dd[@class='name']/a/text()").extract_first()
            item['name'] = name.encode(encoding='UTF-8', errors='strict')
            item['like_num'] = gift.xpath(".//a[@class='likebut']/@rel").extract_first()
            item['price'] = gift.xpath(".//span[@class='m-num']/text()").extract_first()
            item['img_url'] = [gift.xpath(".//a[@class='img-h']//img[@class='lazy']/@data-original").extract_first()]
            item['detail'] = ""
            items_url = self.host_url + gift.xpath(".//a[@class='img-h']/@href").extract_first()
            yield scrapy.Request(url=items_url, meta={"item": item}, callback=self.parse_detail)

    def parse_detail(self, response):
        item = response.meta['item']
        detail = response.xpath("//div[@class='pro_tips']/text()").extract_first()
        print(item['id'])
        item['detail'] = detail
        yield item
