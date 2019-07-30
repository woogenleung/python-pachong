#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
Date:2019年07月30日
author:woogen
'''
import requests
import pymongo
import re

from lxml import etree
from font import ParseFontClass


class DianPingSpider:
    def __init__(self, url):
        """

        :param url:
        """
        self.url = url
        self.client = pymongo.MongoClient(host='localhost', port=27017)
        self.db = self.client.pachong
        self.coll = self.db.dianping
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36',
            'Cookie': '_lxsdk_cuid=16c26ed5d85c8-088c7c9ad9c7e3-37667c02-13c680-16c26ed5d85c8; _lxsdk=16c26ed5d85c8-088c7c9ad9c7e3-37667c02-13c680-16c26ed5d85c8; _hc.v=09b3f69d-517f-2d6b-0909-b6faabdf2654.1564021186; cy=4; cye=guangzhou; thirdtoken=509c3a16-c3d3-4f8d-8e31-00774e31f91e; _thirdu.c=30f604af8e98e35e39c52956ba54ef4f; dper=7dd5c5dcc43ebae3c9a58bf72589a46875f09d4ee4637c0c9123414ce89ac45b983dcd9c3bd393fff251a4fe4a43228555775ad9794c0ead7cb1dab87a3d2ca34cefc515f475b3842bdd12663e881082385d263da25b6a9f3a380bdf6bce088f; ll=7fd06e815b796be3df069dec7836c3df; ua=dpuser_6296148486; ctu=5e7b8c2bd9999abbd4d06d88a1c821b0b22fc79c654c19e6944f2a43a6dceb61; s_ViewType=10; _lx_utm=utm_source%3DBaidu%26utm_medium%3Dorganic; _lxsdk_s=16c4168621a-16f-342-177%7C%7C347'}

    def get_font_css(self, text):
        """
        获取字体
        :param text:
        :return:
        """
        pattern = re.compile(r'href="//(s3plus\.meituan\.net.*?)"')
        result = re.findall(pattern, text)[0]
        font_css_url = result
        print(font_css_url)
        parsefont = ParseFontClass('http://' + font_css_url)
        return parsefont

    def get_html(self):
        """
        获取网页源码并替换
        :return:
        """
        response = requests.get(self.url, headers=self.headers).text
        parsefont = self.get_font_css(response)
        pattern = re.compile(r'(&#x.*?;)')
        # 找到所有字体源码
        font_a = re.findall(pattern, response)
        font_b = []
        # 循环遍历所有的字体源码转化为对应的文字
        for i in font_a:
            data = parsefont.parse_ttf(i)
            font_b.append(data)
        # 替换文字
        for a, b in zip(font_a, font_b):
            response = response.replace(a, b)
        self.parse_html(response)

    def parse_html(self, response):
        """
        解析
        :param response:
        :return:
        """
        html = etree.HTML(response)
        shop_list = html.xpath('//div[contains(@class,"shop-list")]/ul/li/div[@class="txt"]')
        for shop in shop_list:
            shop_name = shop.xpath('div[@class="tit"]/a/h4/text()')[0]
            shop_star = shop.xpath('div[@class="comment"]/span/@title')[0]
            comment_count = shop.xpath('div[@class="comment"]/a[1]//text()')
            cost_avg = shop.xpath('div[@class="comment"]/a[2]/b//text()')
            category = shop.xpath('div[@class="tag-addr"]/a[1]/span//text()')
            shop_addr1 = shop.xpath('div[@class="tag-addr"]/a[2]/span//text()')
            shop_addr2 = shop.xpath('div[@class="tag-addr"]/span//text()')
            shop_addr = ''.join(shop_addr1) + ''.join(shop_addr2)
            one_data = {}
            one_data['店名'] = shop_name
            one_data['评分'] = shop_star
            one_data['评论数'] = ''.join(comment_count).replace('\n', '').strip()
            one_data['人均花费'] = ''.join(cost_avg).replace('\n', '').strip()
            one_data['菜品类型'] = ''.join(category).replace('\n', '').strip()
            one_data['菜品类型'] = ''.join(category).replace('\n', '').strip()
            one_data['店铺地址'] = shop_addr
            print(one_data)

    def start(self):
        self.get_html()


if __name__ == '__main__':
    spider = DianPingSpider('http://www.dianping.com/guangzhou/ch10/r13880')
    spider.start()
