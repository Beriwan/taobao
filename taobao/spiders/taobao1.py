# -*- coding: utf-8 -*-
import scrapy
import json
from redis import Redis
from scrapy_redis.spiders import RedisSpider

from taobao.items import TaobaoItem
import re
import os


class Taobao1Spider(RedisSpider):
    name = 'taobao1'
    redis_key = 'urls:test1'
    count = 1
    r = Redis(host='118.126.100.56', port=6379, db=0)

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domans = filter(None, domain.split(','))
        super(Taobao1Spider, self).__init__(*args, **kwargs)

    def parse(self, response):
        print(str(self.count) + '===============================================')
        content = json.loads(response.text)
        ret = content.get('ret')
        print(response.url)
        if re.match(r'FAIL_SYS_USER_VALIDATE:', ret[0]):
            print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
            self.r.lpush('urls:test1', response.url)
        if 'item' in content['data'].keys():
            item = TaobaoItem()
            item['id'] = content['data']['item']['itemId']
            item['content'] = response.text
            item['title'] = content['data']['item']['title']
            # print(content['data']['item']['title'])
            yield item
        else:
            print('下架===============================================')

        self.count += 1
