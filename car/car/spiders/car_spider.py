# -*- coding: utf-8 -*-
import scrapy


class CarSpiderSpider(scrapy.Spider):
    name = 'car_spider'
    allowed_domains = ['https://www.cn357.com/notice_300']
    start_urls = ['http://https://www.cn357.com/notice_300/']

    def parse(self, response):
        pass
