# -*- coding: utf-8 -*-
import scrapy
from city58_spider.items import City58SpiderItem
from scrapy_redis.spiders import RedisSpider


class City58Spider(RedisSpider):
    name = 'city58'
    # allowed_domains = ['www.xxx.com']
    # start_urls = ['http://bj.58.com/chuzu/pn1/?PGTID=0d3090a7-0000-1fd7-9c9a-3a83d8c87059&ClickID=2']
    redis_key = 'city58'


    # http://bj.58.com/chuzu/pn5/?PGTID=0d3090a7-0000-1fd7-9c9a-3a83d8c87059&ClickID=2
    def parse(self, response):
        """
        获取首页数据，解析70个页码对应的url，进行全站信息爬取
        :param response:
        :return:
        """
        for i in range(2, 70):
            next_url = 'http://bj.58.com/chuzu/pn{}/?PGTID=0d3090a7-0000-1fd7-9c9a-3a83d8c87059&ClickID=2'.format(i)
            yield scrapy.Request(next_url, callback=self.parse_second)

    def parse_second(self, response):
        """
        此回调函数对parse返回的页码页面，进行租房信息的爬取
        :param response:
        :return:
        """
        print(response)
        item = City58SpiderItem()
        titles = response.xpath('//ul[@class="listUl"]/li/div[2]/h2/a/text()').extract()
        rooms = response.xpath('//ul[@class="listUl"]/li/div[2]/p[1]/text()').extract()
        adds = response.xpath('//ul[@class="listUl"]/li/div[2]/p[2]/a/text()').extract()
        prices = response.xpath('//ul[@class="listUl"]/li/div[3]/div[2]/b/text()').extract()
        print(item, titles)
        for i in range(0, len(prices)):
            title = titles[i].replace('\n', '').replace(' ', '')
            if title == '':
                title = 'mjx'
            else:
                item['title'] = title
            item['room'] = rooms[i].replace('\xa0', '').replace(' ', '')
            item['add'] = adds[i].replace('.', '')
            item['price'] = prices[i]
            yield item
