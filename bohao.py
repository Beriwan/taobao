import subprocess
import re

import requests
from requests import ReadTimeout

from taobao.ipdb import *
import redis

ADSL_IFNAME = 'adsl-stop;adsl-start'


def remove_proxy():
    """
    移除代理
    :return: None
    """
    redis = RedisClient()
    redis.remove('adsl1')
    print('Successfully Removed Proxy')


def set_proxy(proxy):
    """
    设置代理
    :param proxy: 代理
    :return: None
    """
    redis = RedisClient()
    if redis.set('adsl1', proxy):
        print('Successfully Set Proxy', proxy)


# def test_proxy(self, proxy):
#     """
#     测试代理
#     :param proxy: 代理
#     :return: 测试结果
#     """
#     try:
#         response = requests.get('www.baidu.com', proxies={
#             'http': 'http://' + proxy,
#             'https': 'https://' + proxy
#         }, timeout=10)
#         if response.status_code == 200:
#             return True
#     except (ConnectionError, ReadTimeout):
#         return False


def get_ip():
    (status, output) = subprocess.getstatusoutput('pppoe-status')
    if status == 0:
        pattern = re.compile('ppp0' + '.*?inet.*?(\d+\.\d+\.\d+\.\d+).*?peer', re.S)
        result = re.search(pattern, output)
        if result:
            ip = result.group(1)
            return ip


def main():
    remove_proxy()
    (status, output) = subprocess.getstatusoutput(ADSL_IFNAME)
    if status == 0:
        print('ADSL Successfully')
        ip = get_ip()
        if ip:
            print('ip is:' + ip)
            proxy = '{ip}:{port}'.format(ip=ip, port=8888)
            set_proxy(proxy)
        else:
            print('get ip failed')
    else:
        print('ADSL Failed, Please Check')


if __name__ == '__main__':
    main()
