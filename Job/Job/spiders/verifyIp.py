# coding:utf-8
import requests
import redis


def is_valid_proxy(ip, port):
    url = 'https://www.lagou.com/'
    proxies = {
           'https': 'https://' + str(ip) + ':' + str(port),
        }

    try:
        ret = requests.get(url, proxies=proxies, timeout=5)
    except Exception, e:
        print e
        return False

    if 200 <= ret.status_code < 300:
        return True
    else:
        return False


if __name__ == '__main__':
    print is_valid_proxy('120.78.15.63', 80)
