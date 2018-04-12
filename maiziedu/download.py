# coding:utf-8
import requests
from bs4 import BeautifulSoup
import os
import re
import urllib2


class Download:
    def __init__(self, lesson_no, video_url, file_path):
        '''
        :param lesson_no: 课程编号
        :param video_url: 视频真实地址
        :param file_path: 视频存储路径
        '''
        self.title_url = 'http://www.maiziedu.com/course/{lesson_no}/'.format(lesson_no=lesson_no)
        self.video_url = video_url
        self.file_path = file_path

    def filename_format(self, filename):
        filename = re.sub('\s', '', filename)  # 去除所有空白字符
        return re.sub(r'\d+:\d+', '', filename)  # 去除filename的时间

    def get_titles(self):
        html = requests.get(self.title_url).content

        titles = [li.text for li in BeautifulSoup(html, 'lxml').find('ul', class_='lesson-lists').find_all('li')]

        assert titles, 'No lesson can be found in url({url})'.format(url=self.title_url)

        return map(self.filename_format, titles)

    def get_size(self, url):
        req = urllib2.Request(url)
        f = urllib2.urlopen(req)
        return round(int(dict(f.headers)['content-length']) * 1.0 / 10 ** 6, 1)   # 单位: M

    def download(self):
        if not os.path.isdir(self.file_path):
            os.mkdir(self.file_path)

        for title in self.get_titles():
            num_str = re.findall(r'(\d+)\.', title)[0]
            file_name = os.path.split(self.video_url)[1]
            file_prefix = os.path.splitext(file_name)[0]
            num = re.findall(r'\d+', file_prefix)[-1]
            if len(num) > 1:
                num_str = num_str.zfill(2)
            new_file_prefix = file_prefix[::-1].replace(num[::-1], num_str[::-1], 1)[::-1]
            download_url = self.video_url.replace(file_prefix, new_file_prefix)  # download url

            save_file_name = title + '.mp4'  # filename
            save_file_path = os.path.join(self.file_path, save_file_name)

            if os.path.exists(save_file_path):
                continue

            print download_url
            print str(self.get_size(download_url)) + 'M'

            res = requests.get(download_url, stream=True)
            with open(save_file_path, 'wb') as fp:
                for chunk in res.iter_content(100000):
                    fp.write(chunk)

            print u'下载完成:'+save_file_path


if __name__ == '__main__':
    Download(373, 'http://newoss.maiziedu.com/qiniu/jqxx-01.mp4',
             u'/Users/liuliangjun/学习文档/学习视频/麦子学院机器学习入门').download()

    Download(395, 'http://newoss.maiziedu.com/mongodb_1.mp4',
             u'/Users/liuliangjun/学习文档/学习视频/MongoDB最佳实践').download()

    Download(1038, 'http://newoss.maiziedu.com/mgxxsjk/mgxxsjk1.mp4',
             u'/Users/liuliangjun/学习文档/学习视频/MySQL入门').download()

    Download(335, 'http://newoss.maiziedu.com/qiniu/jinjie1.mp4',
             u'/Users/liuliangjun/学习文档/学习视频/MySQL进阶').download()


