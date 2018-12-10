import scrapy


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

            if name is None:
                print(response.body)

            yield {
                'name': name,
                'category': cigarette.xpath('.//div[@class="type"]/p/text()').extract(),
                'tarContent': cigarette.xpath('.//div[@class="tar"]/p/text()').extract(),
                'price': cigarette.xpath('.//div[@class="price"]/p/text()').extract(),
                'img': cigarette.xpath('.//div[@class="img"]/img/@src').extract_first(),
            }

        next_page_url = response.xpath('//a[contains(text(),"下一页")]/@href').extract_first()
        if next_page_url is not None:
            yield scrapy.Request(response.urljoin(next_page_url))
