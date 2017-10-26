# -*- coding: utf-8 -*-
import scrapy
from verifyIp import is_valid_proxy
import redis


class CatchProxyIpSpider(scrapy.Spider):
    name = 'catchProxyIp'
    allowed_domains = ['http://www.xicidaili.com/']
    #start_urls = ['http://www.xicidaili.com/nn//1']
    start_urls = ['http://www.xicidaili.com/nn//'+str(i+1) for i in xrange(20)]
    r = redis.Redis(host='localhost', port=6379, db=0)

    def parse(self, response):
        all = response.css('#ip_list tr')
        for a in all[1:]:
            ip = a.css('td:nth-child(2)::text').extract_first(default=None)
            port = a.css('td:nth-child(3)::text').extract_first(default=None)
            live = a.css('td:nth-last-child(2)::text').extract_first(default=None)
            verify_time = a.css('td:last-child::text').extract_first(default=None)
            http_type = a.css('td:nth-child(6)::text').extract_first(default=None)
            if http_type == 'HTTPS':
                print ip, port, live, verify_time, http_type
                ret = is_valid_proxy(ip, port)
                if ret:
                    # self.r.rpush('ip', ip+':'+str(port))
                    print ip+':'+str(port)


if __name__ == '__main__':
    # print is_valid_proxy('120.78.15.63', 80)
    # CatchProxyIpSpider()
    pass