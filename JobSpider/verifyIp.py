# coding:utf-8
import requests
import redis
import re


def is_valid_proxy(ip, url):
    proxies = {
        'http': 'http://'+ip,
        'https': 'https://'+ip
    }
    try:
        ret = requests.get(url, proxies=proxies, timeout=35)
        print ret.text
    except Exception, e:
        print e
        return False

    if 200 <= ret.status_code < 300:
        return True
    else:
        return False


def is_valid_proxy_v2(ip):
    url = 'https://www.lagou.com/'
    proxies = {
        'http': 'http://'+ip,
        'https': 'https://'+ip
    }
    try:
        ret = requests.get(url, proxies=proxies, timeout=35)
        print ret.text
    except Exception, e:
        print e
        return False

    if 200 <= ret.status_code < 300:
        return ip
    else:
        return False


def catch_ip():
    """
    http://www.89ip.cn/apijk/?&tqsl=100&sxa=&sxb=&tta=&ports=&ktip=&cf=1
    """
    headers = {
        'Host': 'www.89ip.cn',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0',
        'Connection': 'keep-alive',
    }

    url = 'http://www.89ip.cn/apijk/?&tqsl=1000&sxa=&sxb=&tta=&ports=&ktip=&cf=1'
    ret = requests.get(url, headers=headers)
    ips = re.findall(r'>([0-9.:]+)<', ret.text, flags=re.DOTALL)
    print ips
    if ips:
        con = redis.Redis()
        con.rpush('boss', *ips)
        con.rpush('lagou', *ips)
        return len(ips)
    return False


if __name__ == '__main__':
    # print is_valid_proxy('190.183.61.157:8080')
    # catch_ip()
    # pass
    # url = ['https://www.zhipin.com/c101010100/h_101010100/?query=Python&page={page}&ka=page-{page}'.format(page=str(i)) for i+1 in
    #        xrange(30)]
    # url = ['https://www.zhipin.com/c101010100-p100104/?page={page}&ka=page-{page}'.format(page=str(i+1)) for i in
    #        xrange(30)]
    # for u in url:
    #     print u
    pass