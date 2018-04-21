# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime
from scrapy.exceptions import DropItem
import re
import os


class WritePipeline(object):

    def process_item(self, item, spider):
        pwd = os.getcwd()
        print(item['title'])
        now = datetime.now()
        time = now.strftime('%Y')+'年'+now.strftime('%m')+'月' + now.strftime('%d') + \
            '日'+now.strftime('%H')+'时'+now.strftime('%M') + \
            '分'+now.strftime('%S')+'秒'
        with open(pwd+'/shuju/{time}_{id}.txt'.format(id=item['id'], time=time), 'w', encoding='utf-8') as f:
            f.write(item['content'])
            print('写入成功')
        return item


class DropPipeline(object):
    """docstring for DropPipeline"""

    def __init__(self):
        self.re_drop = re.compile(r'redirectUrl')

    def process_item(self, item, spider):
        if item['content']:
            if self.re_drop.search(item['content']):
                raise DropItem('商品id: {id} 已下架'.format(id=item['id']))
            else:
                return item
