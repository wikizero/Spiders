# coding:utf-8
from MyRedisQueue import MyRedisQueue
import time
from boss import Boss
from lagou import Lagou
import schedule


class Main:
    def __init__(self):
        self.mrq = MyRedisQueue()
        self.boss_obj = Boss()
        self.lagou_obj = Lagou()

        self.boss_key = 'boss'
        self.boss_task_level = 2
        self.boss_url_level = 1

        self.lagou_key = 'lagou'
        self.lagou_task_level = 2
        self.lagou_url_level = 1

    def boss_worker(self):
        while True:
            task_type, task = self.mrq.pop_task(keys=[self.boss_key])
            print task_type, task
            level = task_type.split('-')[-1]

            if level == str(self.boss_task_level):
                detail_urls = self.boss_obj.get_position_url(task)  # 获取职位详细信息的url
                self.mrq.push_task(self.boss_key, detail_urls, self.boss_url_level)

            elif level == str(self.boss_url_level):
                self.boss_obj.position_detail(task)  # 获取每个职位的信息

            time.sleep(15)  # 控制每隔10秒访问一次

    def lagou_worker(self):
        while True:
            task_type, task = self.mrq.pop_task(keys=[self.lagou_key])
            print task_type, task
            level = task_type.split('-')[-1]

            if level == str(self.lagou_task_level):
                detail_urls = self.lagou_obj.get_position_url(task)  # 获取职位详细信息的url
                self.mrq.push_task(self.lagou_key, detail_urls, self.lagou_url_level)

            elif level == str(self.lagou_url_level):
                self.lagou_obj.position_detail(task)  # 获取每个职位的信息

            time.sleep(15)  # 控制每隔10秒访问一次

    def boss_task(self):
        pos_lst = ['Python', 'Python爬虫', 'Python数据分析', '机器学习', '数据挖掘', '大数据']
        url_str = 'https://www.zhipin.com/c100010000/h_100010000/?query={pos}&page={page}&ka=page-{page}'
        url = [url_str.format(page=str(i + 1), pos=p) for p in pos_lst for i in xrange(1)]
        self.mrq.push_task(self.boss_key, url, level=self.boss_task_level)

    def lagou_task(self):
        pos_lst = ['Python', 'shujuwajue']
        url = []
        for p in pos_lst:
            url += ['https://www.lagou.com/zhaopin/{pos}/{page}/'.format(pos=p, page=str(i + 1)) for i in xrange(5)]
        self.mrq.push_task(self.lagou_key, url, level=self.lagou_task_level)


if __name__ == '__main__':
    # Main().boss_task()
    Main().boss_worker()

    # Main().lagou_task()
    # Main().lagou_worker()

    # schedule.every().day.at("10:30").do(job)