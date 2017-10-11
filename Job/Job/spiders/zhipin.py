# -*- coding: utf-8 -*-
import scrapy
from scrapy.http import Request
import time

class ZhipinSpider(scrapy.Spider):
    name = 'zhipin'
    allowed_domains = ['https://www.zhipin.com']
    labels = ['Python']
    start_urls = ['https://www.zhipin.com/job_detail/?query='+ label +'&scity=101010100&source=2' for label in labels]

    def parse(self, response):
        content = response.css('.info-primary a::attr(href)')
        headers = response.headers
        for one in content:
            link =self.allowed_domains[0] + one.extract()
            time.sleep(0.5)
            if link:
                yield Request(link, callback=self.parse_info, dont_filter=True, headers=headers)

    def parse_info(self, response):
        position = response.css('.info-primary .name::text').extract()[0]
        salary = response.css('.info-primary .badge::text').extract()[0]
        address = response.css('.info-primary p::text').extract()
        print position, salary
        print address
        #position = position_label.xpath('following::text()').extract_first(default='').strip()
        #print position
