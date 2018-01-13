# coding:utf-8
from apscheduler.schedulers.blocking import BlockingScheduler
import Lagou, Boss
from RedisQueue import RedisQueue

sched = BlockingScheduler()


@sched.scheduled_job('cron', hour=23, minute=30)
def start_boss_task():
    pos_lst = ['JAVA', 'C', 'Python', 'PHP', 'IOS', 'Android']
    url = ['https://www.zhipin.com/c101010100-p100104/?page={page}&ka=page-{page}'.format(page=str(i + 1)) for i in
           xrange(2)]
    for p in pos_lst:
        url += ['https://www.zhipin.com/c101010100/h_101010100/?query={pos}&page={page}&ka=page-{page}'.format(
            page=str(i + 1), pos=p) for i in xrange(2)]

    rq = RedisQueue()
    rq.push_task('boss_root', url, level=2)


@sched.scheduled_job('cron', hour=12, minute=30)
def start_lagou_task():
    pass

sched.start()