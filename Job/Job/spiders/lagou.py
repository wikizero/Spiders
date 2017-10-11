# -*- coding: utf-8 -*-
import scrapy
import time
from scrapy.http import Request


class LagouSpider(scrapy.Spider):
    name = 'lagou'
    allowed_domains = ['https://www.lagou.com']
    labels = ['Python']
    start_urls = ['https://www.lagou.com/zhaopin/' + label + '/?utm_source=m_cf_cpt_baidu_pc' for label in labels]
    print start_urls

    def parse(self, response):
        content = response.css('.position_link::attr(href)').extract()
        cookies = response.request.headers
        headers = response.headers
        for link in content:
            #print headers
            time.sleep(0.5)
            # Request set cookies
            yield Request(link, headers=headers, callback=self.parse_info, dont_filter=True)

    def parse_info(self, response):
        position = response.css('.job-name .name::text').extract()
        if not position:
            return False
        print position[0] 
