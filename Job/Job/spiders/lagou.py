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
        headers = response.headers

        next_page = response.css('.pager_container a:last-child::attr(href)').extract()
        print next_page
        if 'www.lagou.com' in next_page:
            yield Request(next_page, headers=headers, callback=self.parse, dont_filter=True)

        for link in content:
            yield Request(link, headers=headers, callback=self.parse_info, dont_filter=True)


    def parse_info(self, response):
        position = response.css('.job-name .name::text').extract()
        if not position:
            return False
        print position[0] 
