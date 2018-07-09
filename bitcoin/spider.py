# coding:utf-8
import requests
import pandas as pd
from bs4 import BeautifulSoup
import sys

reload(sys)
sys.setdefaultencoding('utf-8')


def send_request(url):
    response = requests.get(url=url)
    text = response.text
    return BeautifulSoup(text, 'lxml')


def catch(n=1, filename='output.csv'):
    start_urls = ['https://www.feixiaohao.com/list_{}.html'.format(i) for i in range(1, n + 1)]
    detail_url_str = 'https://www.feixiaohao.com/coindetails/{}/'

    coin_ids = []
    for url in start_urls:
        coin_ids += [row.attrs['id'] for row in send_request(url).select('#table tr')[1:]]

    ret = []
    detail_urls = [detail_url_str.format(c_id) for c_id in coin_ids]
    for url in detail_urls:
        print url
        ret.append([row.text for row in send_request(url).select('.baseInfoList .text')[:4]])

    df = pd.DataFrame(data=ret, columns=[u'英文名', u'中文名', u'上架交易所', u'发行时间'])
    df.to_csv(filename)


if __name__ == '__main__':
    catch(1, filename='output.csv')  # 1页数据， 存入output.csv文件
