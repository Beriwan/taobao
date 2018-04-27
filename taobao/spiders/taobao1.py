# -*- coding: utf-8 -*-
import subprocess
import time

import scrapy
import json
from redis import Redis
from scrapy_redis.spiders import RedisSpider
from datetime import datetime
from taobao.items import TaobaoItem
import re
import os

from taobao.settings import *


class Taobao1Spider(RedisSpider):
    name = 'taobao1'
    redis_key = 'urls:test1'
    count = 1
    r = Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)

    def __init__(self, *args, **kwargs):
        domain = kwargs.pop('domain', '')
        self.allowed_domans = filter(None, domain.split(','))
        super(Taobao1Spider, self).__init__(*args, **kwargs)

    def parse(self, response):
        print(str(self.count) + '===============================================')
        content = json.loads(response.text)
        ret = content.get('ret')
        re_drop = re.compile(r'redirectUrl')
        print(response.url)
        if re.match(r'FAIL_SYS_USER_VALIDATE:', ret[0]):
            self.r.lpush('urls:test1', response.url)
            print('访问太频繁，重新访问')
            print('开始拨号')
            (status, output) = subprocess.getstatusoutput(ADSL_IFNAME)
            if status == 0:
                print('拨号成功')
            else:
                print('拨号失败，休息一会')
                time.sleep(10)
        if re_drop.search(response.text):
            item = TaobaoItem()
            item['zb_state'] = 1
            item['tb_state'] = 1
            item['itemId'] = re.search('itemNumId%22%3A%22(\d+)', response.url).group(1)
            yield item
            print('商品过期不存在')
        if 'item' in content['data'].keys():
            item = TaobaoItem()
            value = content['data']['apiStack'][0]['value']
            value = json.loads(value)
            if value['trade'].get('hintBanner'):
                item['judge'] = value['trade']['hintBanner']['text']
                if item['judge'] == '已下架' or item['judge'] == '商品已经下架啦~':
                    item['zb_state'] = 1
                    item['tb_state'] = 1
                else:
                    item['zb_state'] = 1
                    item['tb_state'] = 0
            else:
                item['zb_state'] = 1
                item['tb_state'] = 0
            item['itemId'] = content['data']['item']['itemId']
            #item['content'] = response.text
            item['quantity'] = value['skuCore']['sku2info']['0']['quantity']
            item['itemprice'] = value['skuCore']['sku2info']['0']['price']['priceText']
            item['deposittime'] = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            # item['title'] = content['data']['item']['title']
            yield item

        self.count += 1
