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
    change = []
    updata = []
    data = {'goodschange': ''}
    data1 = {'update_goods': ''}
    count_change = 0
    count_updata = 0
    url_change = 'http://zbzs.wanshangtang.com/home/Tbapi/goodschange'
    url_updata = 'http://zbzs.wanshangtang.com/home/Tbapi/update_goods'

    def post_updata(self, dict_item):
        items = {"itemId": dict_item["itemId"], "tb_state": dict_item["tb_state"], "zb_state": dict_item["zb_state"]}

        if self.count_updata < 5:
            self.updata.append(items)
            print(self.updata)
            self.count_updata += 1
            print(self.count_updata)
        if self.count_updata == 5:
            json_updata = json.dumps(self.updata)
            self.data1['update_goods'] = json_updata
            # response = requests.post(self.url_updata, data=self.data1)
            # print(response.text)
            print(self.data1)
            del self.updata[:]
            #self.updata.append(items)
            self.count_updata = 0

    def process_item(self, item, spider):
        dict_item = dict(item)
        self.post_updata(dict_item)
        #dict_item.pop('content')
        if dict_item.get('itemprice'):
            items = {"itemId": dict_item["itemId"], "itemprice": dict_item["itemprice"],
                     "quantity": dict_item["quantity"],'deposittime':dict_item["deposittime"]}
            if self.count_change < 5:
                self.change.append(items)
                self.count_change += 1
            if self.count_change == 5:
                json_change = json.dumps(self.change)
                self.data['goodschange'] = json_change
                # response = requests.post(self.url_change, data=self.data)
                # print(response.text)
                print(self.data)
                del self.change[:]
                #self.change.append(items)
                self.count_change = 0
        return item

    def close_spider(self, spider):
        json_change = json.dumps(self.change)
        json_updata = json.dumps(self.updata)
        self.data['goodschange'] = json_change
        self.data1['update_goods'] = json_updata
        # r_change = requests.post(self.url_change, data=self.data)
        # r_updata = requests.post(self.url_updata, data=self.data1)
        # print('----------------------------------')
        # print(r_change.text)
        # print(r_updata.text)
        print(self.data)
        print(self.data1)
