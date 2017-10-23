# coding:utf-8
import requests
from Tasks import *
from bs4 import BeautifulSoup
import redis
import verifyIp
import re
from datetime import datetime
import pprint
import random
from JobModels import *
import sys

reload(sys)
sys.setdefaultencoding('utf-8')
lst = []

headers = {
    'Host': 'www.lagou.com',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
    'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0',
    'Connection': 'keep-alive',
}


def get_ip():
    with open('proxyIp.txt') as fp:
        ip = random.choice(fp.readlines()).strip()

    if ip in lst:
        return get_ip()
    if verifyIp.is_valid_proxy(ip, 'https://www.lagou.com/'):
        return ip
    else:
        lst.append(ip)
        print 'ip_lst:', len(lst)
        return get_ip()


def send_request(url, times=0):
    times += 1
    if times >= 10:
        return False
    ip = get_ip()
    print ip
    proxies = {
        'http': 'http://'+ip,
        'https': 'https://'+ip
    }
    try:
        ret = requests.get(url, headers=headers, proxies=proxies, timeout=30)
    except Exception, e:
        print e
        lst.append(ip)
        print 'ip_lst:', len(lst)
        return send_request(url, times)

    if 200 <= ret.status_code < 300:
        return ret.text
    else:
        return send_request(url, times)


def main(url):
    text = send_request(url)
    if not text:
        return False
    obj = BeautifulSoup(text, 'lxml')
    return [title.get('href') for title in obj.find_all('a', class_='position_link')]


def info(url):
    if not url:
        return False
    text = send_request(url)
    if not text:
        return False
    obj = BeautifulSoup(text, 'lxml')
    data = {}
    data['url'] = url
    data['source'] = u'拉勾网'
    data['create_date'] = datetime.now()
    data['job_id'] = int(re.findall(r'\d{5,10}', url)[0])
    data['position'] = obj.find('span', class_='name').get_text().strip()
    job_request = [span.string.replace('/', '').strip() for span in obj.find('dd', class_='job_request').find_all('span')]
    data['salary'], data['address'], data['exp'], data['edu'], span = job_request
    data['release_date'] = obj.find('p', class_='publish_time').get_text().split()[0].strip()
    data['company'] = obj.find('h2', class_='fl').contents[0].strip()
    data['desc'] = obj.find('dd', class_='job_bt').div.get_text().strip()
    data['label'] = ';'.join([ul.string.strip() for ul in obj.find('ul', class_='position-label') if ul.string.strip()])
    data['position_type'] = obj.find('ul', class_='c_feature').li.contents[2].strip()
    if not Job.select().where(Job.job_id == data['job_id']):
        Job.insert_many([data]).execute()
        return data['position']


if __name__ == '__main__':
    url = ['https://www.lagou.com/zhaopin/Python/' + str(i+1) + '/' for i in xrange(2)]
    # print url
    for u in url:
        # lagou_url_task.apply_async(args=[u], queue='lagou')
        for i in main(u):
            print info(i)
