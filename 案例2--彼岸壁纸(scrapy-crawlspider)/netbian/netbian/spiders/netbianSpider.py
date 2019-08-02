# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule


class NetbianspiderSpider(CrawlSpider):
    name = 'netbianSpider'
    allowed_domains = ['netbian.com']
    start_urls = ['http://www.netbian.com/weimei/index.htm']

    rules = (
        Rule(LinkExtractor(allow=r'/desk/\d+\.htm'), callback='parse_item', follow=False),
        Rule(LinkExtractor(allow=r'weimei/index_\d+.htm'), follow=True)
    )

    def parse_item(self, response):
        image_url = response.xpath('//div[@class="pic"]/p/a/img/@src').extract()
        image_name = response.xpath('//div[@class="action"]/h1/text()').extract()[0]
        print(image_name)
        yield {
            'image_urls': image_url,
            'image_name': image_name

        }
