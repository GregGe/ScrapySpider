from scrapy import cmdline

if __name__ == '__main__':
    #cmdline.execute("scrapy crawl christmas-gift-xpath -o gift.json".split())
    #cmdline.execute("scrapy crawl christmas-gift-xpath -o gift.csv -t csv".split())
    cmdline.execute("scrapy crawl christmas-giftnav-xpath -o giftnav.csv -t csv".split())
    pass