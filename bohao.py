import subprocess
import re
import redis

ADSL_IFNAME = 'adsl-stop;adsl-start'


def get_ip():
    (status, output) = subprocess.getstatusoutput('pppoe-status')
    if status == 0:
        pattern = re.compile('ppp0' + '.*?inet.*?(\d+\.\d+\.\d+\.\d+).*?peer', re.S)
        result = re.search(pattern, output)
        if result:
            ip = result.group(1)
            return ip


def main():
    (status, output) = subprocess.getstatusoutput(ADSL_IFNAME)
    if status == 0:
        print('ADSL Successfully')
        ip = get_ip()
        if ip:
            print('ip is:' + ip)
        else:
            print('get ip failed')
    else:
        print('ADSL Failed, Please Check')


if __name__ == '__main__':
    main()

