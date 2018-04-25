# coding:utf-8
from bs4 import BeautifulSoup
from datetime import datetime
from retry import retry
import store
import requests
import uniout
import re


class Lagou:
    def __init__(self):
        pass

    @retry(tries=2, delay=30)
    def send_request(self, url):
        headers = {
            'Host': 'www.lagou.com',
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0',
        }
        try:
            ret = requests.get(url, headers=headers, timeout=15)
            return ret.text
        except Exception, e:
            print e

    def get_position_url(self, url):
        text = self.send_request(url)
        if not text:
            return False
        obj = BeautifulSoup(text, 'lxml')
        return [title.get('href') for title in obj.find_all('a', class_='position_link')]

    def position_detail(self, url):
        text = self.send_request(url)
        obj = BeautifulSoup(text, 'lxml')

        data = {}

        data['url'] = url
        data['source'] = u'拉勾网'
        data['create_date'] = datetime.now()
        data['_id'] = int(re.findall(r'\d{5,10}', url)[0])
        data['position'] = obj.find('span', class_='name').get_text().strip()

        job_request = [span.string.replace('/', '').strip() for span in
                       obj.find('dd', class_='job_request').find_all('span')]
        data['salary'], data['address'], data['exp'], data['edu'], span = job_request
        data['release_date'] = obj.find('p', class_='publish_time').get_text().split()[0].strip()
        data['company'] = obj.find('h2', class_='fl').contents[0].strip()
        data['desc'] = obj.find('dd', class_='job_bt').div.get_text().strip()
        data['label'] = [ul.string.strip() for ul in obj.find('ul', class_='position-label') if ul.string.strip()]
        data['position_type'] = obj.find('ul', class_='c_feature').li.contents[2].strip()

        store.save(data)


if __name__ == '__main__':
    pos_lst = ['Java', 'Python', 'C++', 'Android', 'PHP', 'shujuwajue']
    url = []
    for p in pos_lst:
        url += ['https://www.lagou.com/zhaopin/{pos}/{page}/'.format(pos=p, page=str(i+1)) for i in xrange(30)]
    # for u in url:
    #     lagou_url_task.apply_async(args=[u], queue='lagou')
    # url = 'https://www.lagou.com/jobs/3893733.html'
    # Lagou().position_detail(url)
    for u in url:
        print Lagou().get_position_url(u)
        import time
        time.sleep(5)
