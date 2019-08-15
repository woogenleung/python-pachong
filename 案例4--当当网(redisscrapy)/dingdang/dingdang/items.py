# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class DingdangItem(scrapy.Item):
    book_title = scrapy.Field()
    book_desc = scrapy.Field()
    author = scrapy.Field()
    public = scrapy.Field()
    # paihang = scrapy.Field()
    # paihang_num = scrapy.Field()
    price = scrapy.Field()
    e_price = scrapy.Field()
    comment_count = scrapy.Field()
    category = scrapy.Field()
    goodId = scrapy.Field()
    good_rate = scrapy.Field()
    average_score = scrapy.Field()
    crazy_count = scrapy.Field()
    detest_count = scrapy.Field()

