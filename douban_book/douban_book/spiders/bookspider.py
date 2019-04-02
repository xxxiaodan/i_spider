# -*- coding: utf-8 -*-
import scrapy
from ..items import DoubanBookItem

class BookspiderSpider(scrapy.Spider):
    name = 'douban'
    allowed_domains = ['douban.com']
    offset = 0
    url = 'https://book.douban.com/top250?start='
    start_urls = [url + str(offset)]

    def parse(self, response):
        for each in response.xpath('//tr[@class="item"]'):
            item = DoubanBookItem()
            item['name'] = each.xpath('td[2]/div[1]/a/@title').extract()[0]
            item['ratings'] = each.xpath('td[2]/div[2]/span[@class="rating_nums"]/text()').extract()[0]
            book_info = each.xpath('td[2]/p[1]/text()').extract()[0]
            book_info_content = book_info.strip().split(' / ')
            item['author'] = book_info_content[0]
            item['publisher'] = book_info_content[-3]
            item['edition_year'] = book_info_content[-2]
            item['price'] = book_info_content[-1]
            yield item
            print('write over')

        if self.offset < 250:
            self.offset += 25

        yield scrapy.Request(self.url + str(self.offset), callback = self.parse)