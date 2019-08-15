#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import requests
import time
import scrapy
from lxml import etree

from dingdang.items import DingdangItem
from scrapy_redis.spiders import RedisSpider


class DingDangSpider(RedisSpider):
    name = 'DD'
    allowed_domains = ['dangdang.com']
    redis_key = 'DD:start_urls'

    def __init__(self, *args, **kwargs):
        super(DingDangSpider, self).__init__(*args, **kwargs)

    # def start_requests(self):
    #     yield scrapy.Request(url=self.base_url, callback=self.parse, dont_filter=True)

    def parse(self, response):
        """
        获取每一页的所有书籍的详细链接
        :param response:
        :return:
        """

        book_list = response.xpath('//div[@id="search_nature_rg"]/ul/li')

        # 每一页的所有书本链接
        for book in book_list:
            book_url = book.xpath('a/@href').extract_first()

            yield scrapy.Request(book_url, callback=self.parse_detail)

        # 下一页链接
        next_page = response.xpath('//li[@class="next"]/a/@href').extract()[0]
        if next_page is not None:
            next_page_url = 'http://category.dangdang.com' + next_page
            yield scrapy.Request(next_page_url, callback=self.parse)

    def parse_detail(self, response):
        """
        书籍信息页
        :param response:
        :return:
        """
        item = DingdangItem()
        book_title = response.xpath('//div[@class="name_info"]/h1/@title').extract_first()
        book_desc = response.xpath('//div[@class="name_info"]/h2/span[1]/@title').extract_first()
        author = response.xpath('//span[@id="author"]/a[1]/text()').extract_first()
        public = response.xpath('//div[@class="messbox_info"]/span[2]/a/text()').extract_first()
        # paihang = response.xpath('//div[contains(@class,"pinglun")]/span[1]/a/text()').extract_first()
        # paihang_num = response.xpath('//div[contains(@class,"pinglun")]/span[1]/span/text()').extract_first()
        comment_count = response.xpath('//div[contains(@class,"pinglun")]/span[2]/a/text()').extract_first()
        price = response.xpath('//p[@id="dd-price"]//text()').extract()
        price = ''.join(price).strip()[1:]
        e_price = response.xpath('//div[@class="price_e"]/p[2]/a/text()').extract_first()
        category = response.xpath('//*[@id="breadcrumb"]/a[1]/b/text()').extract_first() + '>' + response.xpath(
            '//*[@id="breadcrumb"]/a[2]/text()').extract_first() + '>' + response.xpath(
            '//*[@id="breadcrumb"]/a[3]/text()').extract_first()
        goodid = response.url.split('/')[-1].split('.')[0]
        categoryPath = re.findall(r'"categoryPath":"(.*?)"', response.text)[0]
        pinglun_url = f'http://product.dangdang.com/index.php?r=comment%2Flist&productId={goodid}&categoryPath={categoryPath}&mainProductId={goodid}'
        headers = {
            'User-Agent': "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.1 (KHTML, like Gecko) Chrome/22.0.1207.1 Safari/537.1"
        }
        res = requests.get(pinglun_url, headers=headers)
        data = res.json()
        good_rate = data['data']['list']['summary']['goodRate']
        average_score = data['data']['list']['summary']['average_score']
        crazy_count = data['data']['list']['summary']['total_crazy_count']
        detest_count = data['data']['list']['summary']['total_detest_count']

        item['book_title'] = book_title
        item['book_desc'] = book_desc
        item['author'] = author
        item['public'] = public
        item['comment_count'] = comment_count
        item['price'] = price
        item['e_price'] = e_price
        item['category'] = category
        item['goodId'] = goodid
        item['good_rate'] = good_rate
        item['average_score'] = average_score
        item['crazy_count'] = crazy_count
        item['detest_count'] = detest_count
        yield item






