from redis import Redis

id_url = 'https://acs.m.taobao.com/h5/mtop.taobao.detail.getdetail/6.0/?data=%7B%22itemNumId%22%3A%22{id}%22%7D'
try:
    count = 1
    with open('D:\work\所有商品aa.txt', 'r') as f:
        for id in list(set(f.readlines())):
            r = Redis(host='118.126.100.56', port=6379, db=0)
            r.lpush('urls:test1', id_url.format(id=id.strip()))
            print(count)
            count += 1
except KeyboardInterrupt:
    print('end')
