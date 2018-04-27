import json
from redis import Redis
import requests
from requests import RequestException

id_url = 'https://acs.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?data=%7B%22itemNumId%22%3A%22{id}%22%7D'


def main():
    r = Redis(host='118.126.100.56', port=6379, db=0)
    try:
        response = requests.get('http://zbzs.wanshangtang.com/home/Tbapi/get_goods?g_count=1000')
        if response.status_code == 200:
            text = json.loads(response.text)
            for i in range(0, len(text)):
                print(text[i]['itemId'])
                r.lpush('urls:test1', id_url.format(id=text[i]['itemId'].strip()))
        return None
    except RequestException:
        print('请求索引页出错')
        return None


if __name__ == '__main__':
    main()
