#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
大众点评字体反爬虫
Date:2019年07月29日
author: woogen
"""
import os
import redis
import json
import requests
import re

from fontTools.ttLib import TTFont

from ttfs.font import FONT_LIST

HASH_TABLE = 'dianping:ttf'


class ParseFontClass(object):
    def __init__(self, css_url, redis_host='localhost', redis_port=6379, redis_pass=None):
        """
        redis连接本地
        :param css_url:
        :param redis_host: 主机
        :param redis_port: 端口
        :param redis_pass: redis密码
        """
        if redis_pass:
            # decode_response 自动把二进制转换
            pool = redis.ConnectionPool(host=redis_host, port=redis_port, password=redis_pass, decode_responses=True)
        else:
            pool = redis.ConnectionPool(host=redis_host, port=redis_port, decode_responses=True)

        self.redis = redis.Redis(connection_pool=pool)
        self.css_url = css_url
        self.start()

    def parse_ttf(self, code):
        clean_code = code.replace(';', '')[-4:]
        result_list = self.redis.hmget(HASH_TABLE, ['b57729c8.woff','8ea89125.woff','620c796e.woff','50a6ede5.woff','e40270e6.woff','8dae1f86.woff'])
        for result in result_list:
            json_data = json.loads(result)
            if 'uni' + clean_code in json_data:
                return json_data['uni' + clean_code]
        return False

    def get_ttf(self, css_url):
        """

        :param css_url:
        :return:
        """
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/75.0.3770.142 Safari/537.36'
        }
        response = requests.get(css_url, headers=headers)
        if response.status_code == 200:
            text = response.text
            self.install_ttf(self.get_ttf_urls(text))
        else:
            return None

    def get_ttf_urls(self, text):
        pattern = re.compile(r'url\("//(.*?)"\)')
        urls = re.findall(pattern, text)
        ttf_urls = []
        for url in urls:
            if url not in ttf_urls and '.woff' in url:
                ttf_urls.append(url)
        return ttf_urls

    def install_ttf(self, ttf_urls):
        """
        下载并安装字体
        :return:
        """
        name_list = []

        for url in ttf_urls:
            name = url.split('/')[-1]
            name_list.append(name)
        for name, url in zip(name_list, ttf_urls):
            # 判断是否下载过该字体
            if self.check_hash(name):
                continue
            path = 'ttfs/' + name
            with open(path, 'wb+') as f:
                f.write(requests.get('http://' + url).content)
                font = TTFont(path)
                uni_list = font['cmap'].tables[0].ttFont.getGlyphOrder()
                json_data = json.dumps(dict(zip(uni_list, FONT_LIST)), ensure_ascii=False)
                self.add_hash(name, json_data)
                os.remove('ttfs/' + name)
        print('[INFO]字体下载完成')

    def check_hash(self, name):
        return self.redis.hexists(HASH_TABLE, name)

    def add_hash(self, name, json_data):
        self.redis.hset(HASH_TABLE, name, json_data)

    def start(self):
        self.get_ttf(self.css_url)


if __name__ == '__main__':
    parsefont = ParseFontClass(
        css_url='http://s3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/841ac54343d880c69a9461f7e7851558.css')
    's3plus.meituan.net/v1/mss_0a06a471f9514fc79c981b5466f56b91/svgtextcss/9b94f6a76ba4d1a44f086f7e811eca63.css'
