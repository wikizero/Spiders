# coding:utf-8
import os
from apscheduler.schedulers.blocking import BlockingScheduler
import time

sched = BlockingScheduler()


@sched.scheduled_job('cron', hour=23, minute=30)
def start_boss_task():
	os.system("pkill -9 -f 'Tasks'")
	os.system("pkill -9 -f 'flower'")
	time.sleep(5)
	os.system("nohup celery -A Tasks worker -n worker1 -Q boss -c 1 --loglevel=info > boss.log 2>&1 &")
	time.sleep(5)
	os.system("nohup celery flower -A Tasks --address=0.0.0.0 --port=5555 &")
	time.sleep(5)
	os.system("python catchProxyIp.py")
	time.sleep(2)
	os.system("python verifyip.py")
	time.sleep(2)
	os.system("python Boss.py")


@sched.scheduled_job('cron', hour=12, minute=30)
def start_lagou_task():
	os.system("pkill -9 -f 'Tasks'")
	os.system("pkill -9 -f 'flower'")
	time.sleep(5)
	os.system("nohup celery -A Tasks worker -n worker2 -Q lagou -c 1 --loglevel=info > lagou.log 2>&1 &")
	time.sleep(5)
	os.system("nohup celery flower -A Tasks --address=0.0.0.0 --port=5555 &")
	time.sleep(5)
	os.system("python catchProxyIp.py")
	time.sleep(2)
	os.system("python verifyip.py")
	time.sleep(2)
	os.system("python Lagou.py")


sched.start()