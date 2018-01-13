# coding:utf-8
import requests
import redis
import re
from datetime import datetime
import pprint
import random
import math
from JobModels import *
from Base.MySQLHelper import MySQLHelper
import pymysql as mysql
from pandas import read_sql


class JobAnalysisFunc:
	def __init__(self):
		self.engine = mysql.connect(host="localhost", user="root", passwd="root", db="Jobs", charset='utf8')
		self.helper_engine = MySQLHelper.create_engine('root:root@127.0.0.1:3306/Jobs')

	def analysis(self):
		sql = 'select * from job;'
		df = read_sql(sql, self.engine)
		columns = ['job_id', 'position', 'address', 'company', 'position_type', 'exp', 'edu', 'label', 'salary', 'desc']
		data = df[columns]

		def func_exp(s):
			s = s.replace(u'经验', '')
			s = u'应届生' if u'应届' in s else s
			s = u'不限' if u'不限' in s else s
			return s

		data['exp'] = data['exp'].apply(func_exp)

		def func_edu(s):
			s = u'不限' if u'不限' in s else s
			s = s.replace(u'及以上', '').replace(u'以上', '')
			return s

		data['edu'] = data['edu'].apply(func_edu)

		def func_type(s):
			if re.findall(r'python', s, flags=re.IGNORECASE):
				return 'Python'
			elif re.findall(r'java', s, flags=re.IGNORECASE):
				return 'Java'
			elif re.findall(r'php', s, flags=re.IGNORECASE):
				return 'PHP'
			elif re.findall(r'C', s, flags=re.IGNORECASE):
				return 'C/C++'
			elif re.findall(r'ios', s, flags=re.IGNORECASE):
				return 'iOS'
			elif re.findall(r'android', s, flags=re.IGNORECASE) or u'安卓' in s:
				return 'Android'
			elif re.findall(u'数据分析', s):
				return u'数据分析'
			elif re.findall(u'数据挖掘', s):
				return u'数据挖掘'
			elif re.findall(u'大数据', s):
				return u'大数据'
			else:
				return ''
		data['type'] = data['position'].apply(func_type)

		def func_salary(s):
			ret = re.findall(r'(\d+)k', s, re.IGNORECASE)
			if ret:
				return ret[0] if len(ret) == 1 else int(ret[0]) + (int(ret[1]) - int(ret[0])) / 2
			else:
				return 0
		data['salary'] = data['salary'].apply(func_salary)

		now = datetime.now()
		row, col = data.shape
		data['create_date'] = [now for i in xrange(row)]
		data['update_date'] = [now for i in xrange(row)]
		dcts = data.to_dict(orient='records')
		# MySQLHelper.insert_many('jobanalysis', source=dcts, engine=self.helper_engine, conflict='replace', limit=1000)
		for dct in dcts:
			if not JobAnalysis.select().where(JobAnalysis.job_id == dct['job_id']):
				JobAnalysis.insert_many([dct]).execute()
				print dct['position']
			else:
				JobAnalysis.delete().where(JobAnalysis.job_id == dct['job_id']).execute()
				JobAnalysis.insert_many([dct]).execute()
				print 'update: ', dct['position']

if __name__ == '__main__':
	JobAnalysisFunc().analysis()
	# s = '10k-20k'
	# ret = re.findall(r'(\d+)k', s)
	# print ret[0] if len(ret) == 1 else int(ret[0]) + (int(ret[1])-int(ret[0]))/2

