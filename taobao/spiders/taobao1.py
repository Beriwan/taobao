# -*- coding: utf-8 -*-
import scrapy
import json
from taobao.items import TaobaoItem
import re
import os


class Taobao1Spider(scrapy.Spider):
    name = 'taobao1'
    allowed_domains = ['taobao.com']
    start_urls = ['http://taobao.com/']

    id_url = 'https://acs.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?data=%7B%22itemNumId%22%3A%22{id}%22%7D'

    def start_requests(self):
        count = 1
        pwd = os.getcwd()
        with open(pwd+'/所有商品.txt', 'r') as f:
            for id in list(set(f.readlines())):
                print(str(count) + '=========================================')
                count = count + 1
                yield scrapy.Request(self.id_url.format(id=id), self.parse_id, meta={'id': id})

    def parse_id(self, response):
        id = response.meta['id'].strip()
        content = json.loads(response.text)
        ret = content.get('ret')
        if re.match(r'FAIL_SYS_USER_VALIDATE:', ret[0]):
            print('aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
            yield scrapy.Request(self.id_url.format(id=id), self.parse_id, meta={'id': id})
        if 'item' in content['data'].keys():
            item = TaobaoItem()
            item['id'] = id
            item['content'] = response.text
            item['title'] = content['data']['item']['title']
            #print(content['data']['item']['title'])
            yield item
        else:
            print('下架===============================================')
