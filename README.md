# ScrapySpider

## 1. 初始化一个SpiderBot

### 1.1 初始化project
```bash
scrapy startproject projectname
```

### 1.2 创建方便执行的入口
```python
from scrapy import cmdline

if __name__ == '__main__':
    cmdline.execute("scrapy crawl cigarette-xpath -o cigarette.json".split())
```

### 1.3 创建Spider
```python
import scrapy

class GiftSpieder(scrapy.Spider):
    name = "gift-xpath"
    allowed_domins = "cocodiy.com"

    start_urls = {
        'https://www.cocodiy.com'
    }

    def parse(self, response):
        
        pass
```

