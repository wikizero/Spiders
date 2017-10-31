# coding:utf-8
import requests
from pyquery import PyQuery
import pandas as pd
from Base import PandasHelper
import redis
import time


class CatchProxyIp:
	def __init__(self):
		self.headers = {
			'Host': '',
			'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
			'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
			'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; WOW64; rv:56.0) Gecko/20100101 Firefox/56.0',
			'Connection': 'keep-alive',
		}

	def save_proxy_ip(self, ips):
		con = redis.Redis()
		con.rpush('boss', *ips)
		con.rpush('lagou', *ips)

	# 云代理 www.ip3366.net  24小时更新一次 （100条）
	def cloud_proxy(self):
		try:
			header = self.headers.copy()
			header['Host'] = 'www.ip3366.net'
			urls = ['http://www.ip3366.net/free/?stype=1&page={page}'.format(page=str(i)) for i in xrange(1, 8)]
			frames = []
			for link in urls:
				time.sleep(1)
				ret = requests.get(link, headers=header)
				ret.encoding = 'gb2312'
				df = pd.read_html(io=ret.content, header=0)[0]
				frames.append(df)
			df = pd.concat(frames)
			ip_lst = PandasHelper.merge_col(df[['IP', 'PORT']], None, ':').tolist()
			self.save_proxy_ip(ip_lst)
			print 'cloud_proxy:', len(ip_lst)
		except Exception, e:
			print e

	# http://www.ip181.com/  10分钟更新一次 高质量代理 (100条)
	def ip181_proxy(self):
		try:
			header = self.headers.copy()
			header['Host'] = 'www.ip181.com'
			url = 'http://www.ip181.com/'
			ret = requests.get(url, headers=header)
			ret.encoding = 'gb2312'
			df = pd.read_html(io=ret.content, header=0)[0]
			ip_lst = PandasHelper.merge_col(df[[u'IP地址', u'端口']], None, ':').tolist()
			self.save_proxy_ip(ip_lst)
			print 'ip181_proxy:', len(ip_lst)
		except Exception, e:
			print e

	# http://www.ip181.com/daili/1.html 几百页免费代理 (50000+条)
	def ip181_proxy_free(self):
		try:
			header = self.headers.copy()
			header['Host'] = 'www.ip181.com'
			urls = ['http://www.ip181.com/daili/{page}.html'.format(page=str(i)) for i in xrange(1, 5)]
			frames = []
			for link in urls:
				time.sleep(1)
				ret = requests.get(link, headers=header)
				ret.encoding = 'gb2312'
				df = pd.read_html(io=ret.content, header=0)[0]
				frames.append(df)
			df = pd.concat(frames)
			ip_lst = PandasHelper.merge_col(df[[u'IP地址', u'端口']], None, ':').tolist()
			self.save_proxy_ip(ip_lst)
			print 'ip181_proxy_free:', len(ip_lst)
		except Exception, e:
			print e

	# http://www.goubanjia.com/free/gngn/index.shtml 上百页免费代理 （20000+条）
	def goubanjia_proxy_free(self):
		try:
			header = self.headers.copy()
			header['Host'] = 'www.goubanjia.com'
			urls = ['http://www.goubanjia.com/free/gngn/index{page}.shtml'.format(page=str(i)) for i in xrange(1, 5)]
			frames = []
			for link in urls:
				time.sleep(1)
				ret = requests.get(link, headers=header)
				ret.encoding = 'gb2312'
				df = pd.read_html(io=ret.text, header=0)[0]
				frames.append(df)
			df = pd.concat(frames)
			ip_lst = [i.replace('..', '.') for i in df['IP:PORT'].tolist()]
			self.save_proxy_ip(ip_lst)
			print 'goubanjia_proxy_free:', len(ip_lst)
		except Exception, e:
			print e

	# http://www.kuaidaili.com/free/inha/  快代理 几百页免费代理 （20000+）
	def kuai_proxy(self):
		try:
			header = self.headers.copy()
			header['Host'] = 'www.kuaidaili.com'
			urls = ['http://www.kuaidaili.com/free/inha/{page}/'.format(page=str(i)) for i in xrange(1, 5)]
			frames = []
			for link in urls:
				time.sleep(1)
				ret = requests.get(link, headers=header)
				# ret.encoding = 'gb2312'
				df = pd.read_html(io=ret.content, header=0)[0]
				frames.append(df)
			df = pd.concat(frames)
			ip_lst = PandasHelper.merge_col(df[['IP', 'PORT']], None, ':').tolist()
			self.save_proxy_ip(ip_lst)
			print 'kuai_proxy:', len(ip_lst)
		except Exception, e:
			print e


if __name__ == '__main__':
	CatchProxyIp().cloud_proxy()
	CatchProxyIp().ip181_proxy()
	CatchProxyIp().ip181_proxy_free()
	CatchProxyIp().goubanjia_proxy_free()
	CatchProxyIp().kuai_proxy()
