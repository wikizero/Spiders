# coding:utf-8
from bs4 import BeautifulSoup
from datetime import datetime
from MyRedisQueue import MyRedisQueue
from retry import retry
import requests
import uniout
import time
import re

from project.Spiders.Positions import store


class Boss:
    def __init__(self):
        self.base_url = 'https://www.zhipin.com'

    @retry(tries=2, delay=30)
    def send_request(self, url):
        headers = {
            'Host': 'www.zhipin.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0',
        }
        try:
            ret = requests.get(url, headers=headers, timeout=15)
            return ret.text
        except Exception, e:
            print e

    def get_position_url(self, url):
        text = self.send_request(url)
        obj = BeautifulSoup(text, 'lxml')
        links = [self.base_url + div.h3.a.get('href') for div in obj.find_all('div', class_='info-primary')]
        time.sleep(5)
        return links

    def position_detail(self, url):
        print url
        text = self.send_request(url)
        obj = BeautifulSoup(text, 'lxml')

        data = {}

        data['url'] = url
        data['source'] = u'Boss直聘'
        data['create_date'] = datetime.now()
        # data['job_id'] = int(re.findall(r'\d{10,12}', url)[0])  # job_id 更新  2018/4/21
        data['_id'] = obj.find('a', class_='btn-startchat').attrs['ka'].split('_')[-1]

        data['release_date'] = obj.find('span', class_='time').get_text().strip()
        data['company'] = obj.find('div', class_='info-company').h3.a.string.strip()
        data['desc'] = obj.find('div', class_='detail-content').div.div.get_text().strip()
        data['position_type'] = obj.find('div', class_='info-company').p.a.string.strip()

        info_obj = obj.find('div', class_='job-primary')
        data['position'] = info_obj.find('div', class_='name').h1.get_text().strip()
        data['salary'] = info_obj.find('span', class_='badge').get_text().strip()
        data['address'], span, data['exp'], span, data['edu'] = info_obj.find('p').contents
        data['label'] = [span.string for span in info_obj.find('div', class_='job-tags').find_all('span')]

        store.save(data)


if __name__ == '__main__':
    # java c c++
    # 数据挖掘
    pos_lst = ['JAVA', 'C', 'Python', 'PHP', 'IOS', 'Android']
    pos_lst = ['Python']
    url = ['https://www.zhipin.com/c101010100-p100104/?page={page}&ka=page-{page}'.format(page=str(i + 1)) for i in
           xrange(2)]
    for p in pos_lst:
        url += ['https://www.zhipin.com/c101010100/h_101010100/?query={pos}&page={page}&ka=page-{page}'.format(
            page=str(i + 1), pos=p) for i in xrange(2)]

    from pprint import pprint
    from itertools import chain

    # boss = Boss()
    # items = chain.from_iterable(map(boss.get_position_url, url))
    # mrq = MyRedisQueue()
    # mrq.push_task('boss', url, level=2)
    # mrq.push_task('boss', list(items), level=1)

    url = 'https://www.zhipin.com//job_detail/061b056bf9ce324e1n1-29S4FlI~.html'
    Boss().position_detail(url)

    # 列表直接插入（职位标签）更复杂的数据结构
    # _id覆盖
    # db.student.find({"school.name":"西大", "school.city":"南宁"})  key的双引号必须带上
    # 正则表达书查询 db.student.find({name:/^小/})  以小开头的
    # db.student.find({school:{$exists:false}})  不存在学校字段信息的数据
    # db.student.update({}, {$inc:{age:1}}, {multi:true})  # 全体年龄加一(注意：当某个文档没有该字段的时候，会产生一个)

