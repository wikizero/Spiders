# coding:utf-8
import requests
from Tasks import *
from bs4 import BeautifulSoup
import redis
import verifyIp
from Base.MySQLHelper import *
from JobModels import *
import re
from datetime import datetime
import random
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def get_ip():
    con = redis.Redis()
    while True:
        proxy_ip = con.brpop('boss')[1]
        if verifyIp.is_valid_proxy(proxy_ip, 'https://www.zhipin.com'):
            return proxy_ip


def send_request(url, times=0):
    times += 1
    if times >= 50:
        return False
    ip = get_ip()
    print ip
    proxies = {
        'http': 'http://'+ip,
        'https': 'https://'+ip
    }
    headers = {
        'Host': 'www.zhipin.com',
        'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
        'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0',
        'Connection': 'keep-alive',
    }
    try:
        ret = requests.get(url, headers=headers, proxies=proxies, timeout=35)
    except Exception, e:
        print e
        return send_request(url, times)

    if 200 <= ret.status_code < 300:
        text = ret.text
        if text:
            # 该Ip可用 把该IP重新push进redis(从左边push进去)
            con = redis.Redis()
            con.lpush('boss', ip)
            print ip, con.llen('boss')
            return ret.text
        else:
            return send_request(url, times)
    else:
        return send_request(url, times)


def main(url):
    base_url = 'https://www.zhipin.com'
    text = send_request(url)
    if not text:
        return False
    obj = BeautifulSoup(text, 'lxml')
    return [base_url+div.h3.a.get('href') for div in obj.find_all('div', class_='info-primary')]


def info(url):
    if not url:
        return False
    text = send_request(url)
    if not text:
        return False
    obj = BeautifulSoup(text, 'lxml')
    data = {}
    data['url'] = url
    print url
    data['source'] = u'Boss直聘'
    data['create_date'] = datetime.now()
    data['job_id'] = int(re.findall(r'\d{10,12}', url)[0])
    data['release_date'] = obj.find('span', class_='time').get_text().strip()
    data['company'] = obj.find('div', class_='info-company').h3.a.string.strip()
    data['desc'] = obj.find('div', class_='detail-content').div.div.get_text().strip()
    data['position_type'] = obj.find('div', class_='info-company').p.a.string.strip()

    info_obj = obj.find('div', class_='job-primary')
    data['position'] = info_obj.find('div', class_='name').contents[0].strip()
    data['salary'] = info_obj.find('span', class_='badge').get_text().strip()
    data['address'], span, data['exp'], span, data['edu'] = info_obj.find('p').contents
    data['label'] = ';'.join([span.string for span in info_obj.find('div', class_='job-tags').find_all('span')])
    if not Job.select().where(Job.job_id == data['job_id']):
        Job.insert_many([data]).execute()
        return data['position']

if __name__ == '__main__':
    # java c c++
    # 数据挖掘
    #url = ['https://www.zhipin.com/c101010100-p100104/?page={page}&ka=page-{page}'.format(page=str(i+1)) for i in xrange(5)]
    #url = ['https://www.zhipin.com/c101010100/h_101010100/?query=C&page={page}&ka=page-{page}'.format(page=str(i+1)) for i in xrange(5)]
    for u in url:
        boss_url_task.apply_async(args=[u], queue='boss')

