# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from datetime import datetime
from scrapy.exceptions import DropItem
import re
import os
import pymysql
import requests


db_config = {
    'host': '118.126.100.56',
    'port': 3306,
    'user': 'admin',
    'password': '123456',
    'db': 'TEST1',
    'charset': 'utf8'
}


class MysqlPipeline(object):
    # 获取数据库连接和游标
    def __init__(self):
        self.connection = pymysql.connect(**db_config)
        self.cursor = self.connection.cursor()

    def process_item(self, item, spider):
        sql = 'replace into info01(itemid, title) values(%s, %s)'
        try:
            self.cursor.execute(sql, (
                item['id'],
                item['title'],
            )
                                )
            self.connection.commit()
            print('写入Mysql')
        except pymysql.Error as e:
            print(e.args)
        return item


class WritePipeline(object):

    def process_item(self, item, spider):
        pwd = os.getcwd()
        print(item['title'])
        now = datetime.now()
        time = now.strftime('%Y') + '年' + now.strftime('%m') + '月' + now.strftime('%d') + \
               '日' + now.strftime('%H') + '时' + now.strftime('%M') + \
               '分' + now.strftime('%S') + '秒'
        with open(pwd + '/shuju/{time}.txt'.format(time=time), 'w', encoding='utf-8') as f:
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


class PostPipeline(object):
    items = []
    data = {'goodschange': ''}
    count = 0
    url = 'http://zbzs.wanshangtang.com/home/Tbapi/goodschange'

    def process_item(self, item, spider):
        dict_item = dict(item)
        dict_item.pop('content')
        if self.count == 5:
            json_items = json.dumps(self.items)
            self.data['goodschange'] = json_items
            #response = requests.post(self.url, data=self.data)
            #print(response.text)
            print(self.data)
            del self.items[:]
            self.items.append(dict_item)
            self.count = 1
        if self.count < 5:
            self.items.append(dict_item)
            self.count += 1
        return item

    def close_spider(self, spider):
        json_items = json.dumps(self.items)
        self.data['goodschange'] = json_items
        # response = requests.post(self.url, data=self.data)
        # print(response.text)
        print(self.data)

