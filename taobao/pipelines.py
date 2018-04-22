# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from datetime import datetime
from scrapy.exceptions import DropItem
import re
import os
import pymysql

db_config = {
    'host': '127.0.0.1',
    'port': 3306,
    'user': 'root',
    'password': 'woshiren12',
    'db': 'info2',
    'charset': 'utf8'
}


class LgspiderPipeline(object):
    # 获取数据库连接和游标
    def __init__(self):
        self.connection = pymysql.connect(**db_config)
        self.cursor = self.connection.cursor()

    def process_item(self, item, spider):
        sql = 'insert into info01(title, salary, position, time, grade, company) values(%s, %s, %s, %s, %s, %s)'
        try:
            self.cursor.execute(sql, (item['title'].encode('utf-8'),
                                      item['salary'],
                                      item['position'].encode('utf-8'),
                                      item['time'].encode('utf-8'),
                                      item['grade'].encode('utf-8'),
                                      item['company'].encode('utf-8'),
                                      )
                                )
            self.connection.commit()
        except pymysql.Error as e:
            print(e.args)
        return item




class WritePipeline(object):

    def process_item(self, item, spider):
        pwd = os.getcwd()
        print(item['title'])
        now = datetime.now()
        time = now.strftime('%Y')+'年'+now.strftime('%m')+'月' + now.strftime('%d') + \
            '日'+now.strftime('%H')+'时'+now.strftime('%M') + \
            '分'+now.strftime('%S')+'秒'
        with open(pwd+'/shuju/{time}.txt'.format(time=time), 'w', encoding='utf-8') as f:
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
