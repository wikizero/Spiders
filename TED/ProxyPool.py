"""
从各个代理IP网站抓取免费代理IP
1、云代理 www.ip3366.net
2、旗云代理 http://www.qydaili.com/
3、unknown http://www.goubanjia.com
4、快代理 http://www.kuaidaili.com/free/inha/
5、89免费代理 http://www.89ip.cn/index_1.html
6、IP海代理 http://www.iphai.com/free/ng
7、极速代理 http://www.superfastip.com/welcome/freeip/1
8、西刺代理  https://www.xicidaili.com/nn/
9、西拉免费代理IP  http://www.xiladaili.com/https/1/  可用率比较高有反爬限制
10、http://www.nimadaili.com/gaoni/  可用率比较高有反爬限制
11、http://ip.kxdaili.com/ipList/1.html#ip
12、http://31f.cn/
13、http://www.shenjidaili.com/shareip/    http代理(处理方式不一致, 未处理)
14、http://www.66ip.cn/areaindex_19/1.html   有反爬限制，js动态加载
16、http://www.dlnyys.com/free/
"""
import re
from multiprocessing.dummy import Pool

import requests
from faker import Faker
from redis import StrictRedis


class ProxyPool:
    def __init__(self):

        self.redis_key = 'proxy_ip'  # proxy ip 存储在redis的key
        self.max_workers = 3  # 爬虫采用的是线程池，此参数设置最大线程数量
        self.search_depth = 10  # 代理IP资源网站的搜索页数
        self.check_url = 'https://www.baidu.com/'  # proxy ip 有效性校验地址
        self.db = StrictRedis.from_url('redis://localhost:6379/0', decode_responses=True)

        # 匹配proxy ip正则式
        self.pattern_tags = re.compile(r'<[^>]+>', re.S)
        self.pattern_blank = re.compile(r'\s+', re.S)
        self.pattern_colon = re.compile(r' ', re.S)
        self.pattern_ip = re.compile(r'(?:\d+\.){3}\d+:\d+')

    def is_valid_proxy(self, ip, url=None, timeout=5):
        """
        校验代理ip是否能访问指定url（代理ip是否有效）
        :param ip: 127.0.0.1:8888
        :param url: https://www.baidu.com/
        :param timeout: 超时时间
        """
        url = url or self.check_url

        proxies = {
            'http': 'http://' + ip,
            'https': 'https://' + ip
        }

        try:
            ret = requests.get(url, proxies=proxies, timeout=timeout)
        except Exception as e:
            return False

        if 200 <= ret.status_code < 300:
            return ip

    def save_proxy_ip(self, ips: list):
        """
        保存代理ip
        :param ips: list
        :return: None
        """
        p = Pool(10)
        ret = p.map(self.is_valid_proxy, ips)
        proxy_ips = [i for i in ret if i]
        if proxy_ips:
            self.db.lpush(self.redis_key, *proxy_ips)
        return f'Effective rate: {len(proxy_ips)}/{len(ips)}'

    def get_proxy_ip(self):
        """
        单个代理ip获取
        出队后会进行校验，无效的被剔除，有效的反向入队便于下次使用
        :return: ip:port
        """
        while True:
            proxy_ip = self.db.brpop(self.redis_key)[1]
            if self.is_valid_proxy(proxy_ip):
                self.db.lpush(self.redis_key, proxy_ip)
                return proxy_ip

    def send_request(self, url):
        try:
            ret = requests.get(url, headers={'User-Agent': Faker().user_agent()})
            ip_lst = self.extract_proxy_ip(ret.text)
            if ip_lst:
                rate = self.save_proxy_ip(ip_lst)
                print(f'{url} - {rate}')
            else:
                print(f'{url} - No Proxy IP here')
        except Exception as e:
            print(e)

    def extract_proxy_ip(self, html):
        """
        匹配任意html页面的代理IP
        :param html:
        :return:
        """
        # 删除所有html标签
        text = self.pattern_tags.sub('', html)
        # 将空白符替换成空格
        text = self.pattern_blank.sub(' ', text)
        # 两数字之前的空格替换成冒号
        text = self.pattern_colon.sub(':', text)
        # 提取代理ip
        proxy_ip_lst = self.pattern_ip.findall(text)

        return proxy_ip_lst

    def catch(self):
        p = Pool(self.max_workers)
        p.map(self.send_request, self.get_urls())

    def get_urls(self):
        urls = []
        origin_urls = [
            'http://www.nimadaili.com/gaoni/{page}/',
            'http://www.nimadaili.com/http/{page}/',
            'http://www.nimadaili.com/https/{page}/',
            'http://www.xiladaili.com/https/{page}/',
            'http://www.xiladaili.com/putong/{page}/',
            'http://www.xiladaili.com/gaoni/{page}/',
            'http://www.xiladaili.com/https/{page}/',
            'https://www.xicidaili.com/nn/{page}',
            'http://www.superfastip.com/welcome/freeip/{page}',
            'http://www.89ip.cn/index_{page}.html',
            'http://www.kuaidaili.com/free/inha/{page}/',
            'http://www.qydaili.com/free/?action=china&page={page}',
            'http://www.ip3366.net/free/?stype=1&page={page}',
            'http://ip.kxdaili.com/ipList/{page}.html#ip',
            'http://www.dlnyys.com/free/inha/{page}/',

        ]
        for url in origin_urls:
            urls += [url.format(page=i) for i in range(1, self.search_depth)]

        urls.append('http://31f.cn/')
        urls.append('http://www.kxdaili.com/dailiip.html')

        return urls


if __name__ == '__main__':
    # TODO 按自个情况配置 __init__() 参数，再run
    ProxyPool().catch()
