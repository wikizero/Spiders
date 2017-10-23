# coding:utf-8
from peewee import *
from datetime import datetime
db = MySQLDatabase('Jobs', user='root', charset='utf8mb4', password='root', host='localhost')


class Job(Model):
	job_id = IntegerField(primary_key=True)  # time stamp
	position = CharField(max_length=35)
	address = CharField(max_length=15)
	company = CharField(max_length=25)
	position_type = CharField(max_length=25)
	exp = CharField(max_length=15)
	edu = CharField(max_length=10)
	label = CharField(max_length=35)
	salary = CharField(max_length=10)
	desc = TextField()
	url = CharField(max_length=50)
	source = CharField(max_length=10)  # on-sale  sold-out  remove
	release_date = CharField(max_length=20)
	create_date = DateTimeField()

	class Meta:
		database = db


#db.connect()
# db.drop_tables([Job])
#db.create_tables([Job])
