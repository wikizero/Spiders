# coding:utf-8
import requests
from Tasks import *
from bs4 import BeautifulSoup
import redis
import verifyIp

headers = {
	'Host': 'www.zhipin.com',
	'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
	'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
	'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0',
	'Connection': 'keep-alive',
}


def main(url):
	base_url = 'https://www.zhipin.com'
	text = requests.get(url, headers=headers).text
	obj = BeautifulSoup(text, 'lxml')
	return [base_url+div.h3.a.get('href') for div in obj.find_all('div', class_='info-primary')]


def info(url):
	text = requests.get(url, headers=headers).text
	obj = BeautifulSoup(text, 'lxml')
	return obj.find('div', class_='info-primary').get_text().split()[1]


if __name__ == '__main__':
	url = ['https://www.zhipin.com/c101010100/h_101010100/?query=python&page=' + str(i+1) + '&ka=page-5' for i in xrange(2)]
	# print url
	# for u in url:
	# 	print main(u)
	for u in url:
		# boss_url_task.apply_async(args=[u], queue='boss')
		for i in main(u):
			print info(i)
			time.sleep(15)
