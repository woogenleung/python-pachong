# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
from scrapy.conf import settings
import random

# webdriver
# from selenium import webdriver
# from selenium.webdriver.common.by import By
# from selenium.webdriver.support.wait import WebDriverWait
# from selenium.webdriver.support import expected_conditions as EC
# from scrapy.http import HtmlResponse
# import time



class RandomUserAgentMiddleware(object):
    def __init__(self):
        self.userAgent = settings['USER_AGENTS']

    def process_request(self, request, spider):
        userAgent = random.choice(self.userAgent)
        print(f'userAgent: {userAgent}')
        request.headers.setdefault('User-Agent',userAgent)


# class SeleniumMiddleware(object):
#     def __init__(self):
#         print('open chrome')
#         chrome_options = webdriver.ChromeOptions()
#         # 设置中文
#         chrome_options.add_argument('lang=zh_CN.UTF-8')
#
#         # 设置无图加载 1 允许所有图片; 2 阻止所有图片; 3 阻止第三方服务器图片
#         prefs = {
#             'profile.default_content_setting_values': {
#                 'images': 2
#             }
#         }
#         chrome_options.add_experimental_option("prefs", prefs)
#         chrome_options.add_argument('--headless')
#         self.browser = webdriver.Chrome(chrome_options=chrome_options)
#         self.wait = WebDriverWait(self.browser, timeout=15)
#         self.browser.set_page_load_timeout(15)
#
#     def __del__(self):
#         print('close chrome')
#         self.browser.close()
#
#     def process_request(self, request, spider):
#         print(request.url)
#         try:
#             self.browser.get(request.url)
#             time.sleep(2)
#             body = self.browser.page_source
#             return HtmlResponse(url=request.url, body=body, request=request,encoding='utf-8')
#         except Exception as e:
#             print(f'[ERROR]{e}')
#             return HtmlResponse(url=request.url, status=500, request=request)

