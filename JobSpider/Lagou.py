# coding:utf-8
import requests
from Tasks import *
from bs4 import BeautifulSoup
import redis
import verifyIp

headers = {
	'Host': 'www.lagou.com',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0',
	'Connection': 'keep-alive',
}


def main(url):
	text = requests.get(url, headers=headers).text
	obj = BeautifulSoup(text, 'lxml')
	return [title.get('href') for title in obj.find_all('a', class_='position_link')]


def info(url):
	text = requests.get(url, headers=headers).text
	obj = BeautifulSoup(text, 'lxml')
	return obj.find('span', class_='name').get_text()


if __name__ == '__main__':
	url = ['https://www.lagou.com/zhaopin/Python/' + str(i+1) + '/' for i in xrange(30)]
	# print url
	for u in url:
		lagou_url_task.apply_async(args=[u], queue='lagou')