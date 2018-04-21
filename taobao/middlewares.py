# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html

from scrapy import signals
import random
from taobao.settings import USER_AGENTS
import requests


class MyproxisSpiderMidleware(object):
    """docstring for MyproxisSpiderMidleware"""

    def __init__(self, ip=''):
        self.ip = ip

    def get_proxy(self):
        try:
            response = requests.get('http://127.0.0.1:5555/random')
            if response.status_code == 200:
                return response.text
            return None
        except ConnectionError:
            return None

    def get_proxy1(self):
        with open('D:/work/IP代理2.txt', 'r') as f:
            ip = random.choice(f.readlines())
            return ip.strip()

    def process_request(self, request, spider):
        proxy = self.get_proxy()
        print('this is ip:' + proxy)
        request.meta['proxy'] = 'https://'+proxy


class RandomUserAgent(object):
    """docstring for RandomUserAgent"""
    def process_request(self, request, spider):
        useragent = random.choice(USER_AGENTS)
        request.headers.setdefault('User-Agent', useragent)
        