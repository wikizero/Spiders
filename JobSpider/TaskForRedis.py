# coding:utf-8
import Lagou, Boss
from RedisQueue import RedisQueue
import time

if __name__ == '__main__':
    rq = RedisQueue()
    while True:
        try:
            task_type, task = rq.pop_task(['boss_basic', 'lagou_basic', 'boss_info', 'lagou_info'])
            print task_type
            if 'boss_basic' in task_type:
                Boss.main(task)
            elif 'lagou_basic' in task_type:
                pass
            elif 'boss_info' in task_type:
                Boss.info(task)
            elif 'lagou_info' in task_type:
                pass
        except Exception, e:
            print e
        time.sleep(5)

