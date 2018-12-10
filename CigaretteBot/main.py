from scrapy import cmdline

if __name__ == '__main__':
    cmdline.execute("scrapy crawl cigarette-xpath -o cigarette.json".split())