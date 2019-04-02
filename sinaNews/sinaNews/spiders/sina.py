# -*- coding: utf-8 -*-
import scrapy
from sinaNews.items import SinanewsItem
import os


class SinaSpider(scrapy.Spider):
    name = 'sina'
    allowed_domains = ['sina.com.cn']
    start_urls = ['http://news.sina.com.cn/guide/']

    def parse(self, response):
        items = []
        parentUrls = response.xpath('//div[@id="tab01"]/div/h3/a/@href').extract()
        parentTitle = response.xpath('//div[@id="tab01"]/div/h3/a/text()').extract()

        subUrls = response.xpath('//div[@id="tab01"]/div/ul/li/a/@href').extract()
        subTitle = response.xpath('//div[@id="tab01"]/div/ul/li/a/text()').extract()

        for i in range(0, len(parentTitle)):
            parentFilename = './Data/' + parentTitle[i]

            if (not os.path.exists(parentFilename)):
                os.makedirs(parentFilename)

            for j in range(0, len(subUrls)):
                item = SinanewsItem()

                item['parentTitle'] = parentTitle[i]
                item['parentUrls'] = parentUrls[i]

                #检查小类的url是否以同类别大类url开头,如果是返回true
                if_belong = subUrls[j].startswith(item['parentUrls'])
                if if_belong:
                    subFilename = parentFilename + '/' + subTitle[j]
                    if (not os.path.exists(subFilename)):
                        os.makedirs(subFilename)

                item['subUrls'] = subUrls[j]
                item['subTitle'] = subTitle[j]
                item['subFilename'] = subFilename

                items.append(item)

        #发送每个小类url的Request请求，得到Response连同包含meta数据 一同交给econd_parse 方法处理
        for item in items:
            yield scrapy.Request(url=item['subUrls'], meta={'meta_1':item},callback=self.second_parse)

    def second_parse(self,response):
        #提取每次Response的meta数据
        meta_1 = response.meta['meta_1']

        sonUrls = response.xpath('//a/@href').extract()

        items=[]
        for i in range(len(sonUrls)):
            if_belong = sonUrls[i].endswith('.shtml') and sonUrls[i].startswith(meta_1['parentUrls'])

            if(if_belong):
                item = SinanewsItem()
                item['parentTitle'] = meta_1['parentTitle']
                item['parentUrls'] = meta_1['parentUrls']
                item['subUrls'] = meta_1['subUrls']
                item['subTitle'] = meta_1['subTitle']
                item['subFilename'] = meta_1['subFilename']
                item['sonUrls'] = sonUrls[i]
                items.append(item)

            # 发送每个小类下子链接url的Request请求，得到Response后连同包含meta数据 一同交给回调函数 detail_parse 方法处理
        for item in items:
            yield scrapy.Request(url = item['sonUrls'], meta={'meta_2':item}, callback = self.detail_parse)

    #获取文章标题和内容
    def detail_parse(self, response):
        item = response.meta['meta_2']
        content = ''
        head = response.xpath('//h1[@class="main-title"]/text()').extract()
        content_list = response.xpath('//div[@id="article"]/p/text()').extract()

        for i in content_list:
            content += i

        item['head'] = head
        item['content'] = content

        yield item
        print('***detail parse is over***')