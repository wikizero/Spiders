# coding:utf-8
from celery import Celery
import os
import Lagou, Boss
import time

broker = 'redis://127.0.0.1:6379/1'
backend = 'redis://127.0.0.1:6379/2'

app = Celery('tasks', broker=broker, backend=backend)
app.conf.task_routes = {
    'boss.tasks.*': {
        'queue': 'boss',
    },
    'lagou.tasks.*': {
        'queue': 'lagou',
    }
}


@app.task
def lagou_info_task(url):
    return Lagou.info(url)


@app.task
def lagou_url_task(url):
    urls = Lagou.main(url)
    if urls:
        for _url in urls:
            lagou_info_task.apply_async(args=[_url], queue='lagou')
        return 'Success(lagou)'
    else:
        return 'Fail(lagou)'


@app.task
def boss_info_task(url):
    return Boss.info(url)


@app.task
def boss_url_task(url):
    urls = Boss.main(url)
    if urls:
        for _url in urls:
            lagou_info_task.apply_async(args=[_url], queue='boss')
        return 'Success(boss)'
    else:
        return 'Fail(boss)'


if __name__ == '__main__':
    os.system('celery -A Tasks worker -n worker1 -Q boss -c 1  --loglevel=info')
    # os.system('celery -A Tasks worker -n worker2 -Q lagou -c 1  --loglevel=info')
    # os.system('celery flower -A Tasks')
    # pass