import redis
from datetime import datetime
import json

r = redis.Redis(host='118.126.100.56', port=6379, db=0)
while True:
    source, data = r.blpop('taobao1:items')
    now = datetime.now()
    time = now.strftime('%Y')+'年'+now.strftime('%m')+'月' + now.strftime('%d') + \
                '日'+now.strftime('%H')+'时'+now.strftime('%M') + \
                '分'+now.strftime('%S')+'秒'
    try:
        with open('D:work/shuju/{time}.txt'.format(time=time), 'w', encoding='utf-8') as f:
            dict_1 = json.loads(str(data, encoding='utf-8'))
            content = dict_1.get('content')
            id = dict_1.get('id')
            f.write(content)
            print('写入成功id: {id}'.format(id=id))
    except KeyError:
        print('error')


