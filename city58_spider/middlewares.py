# -*- coding: utf-8 -*-

# Define here the models for your spider middleware
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/spider-middleware.html
import random
from scrapy.downloadermiddlewares.useragent import UserAgentMiddleware
from city58_spider.settings import USER_AGENT_LIST
from city58_spider.settings import PROXY_http
from city58_spider.settings import PROXY_https


# UA池代码的编写（单独给UA池封装一个下载中间件的一个类）
# 1，导包UserAgentMiddlware类
class RandomUserAgent(UserAgentMiddleware):

    def process_request(self, request, spider):
        # 从列表中随机抽选出一个ua值
        ua = random.choice(USER_AGENT_LIST)
        # ua值进行当前拦截到请求的ua的写入操作
        request.headers.setdefault('User-Agent', ua)


# 批量对拦截到的请求进行ip更换
class Proxy(object):
    def process_request(self, request, spider):
        # 对拦截到请求的url进行判断（协议头到底是http还是https）
        # request.url返回值：http://www.xxx.com
        h = request.url.split(':')[0]  # 请求的协议头
        if h == 'https':
            ip = random.choice(PROXY_https)
            request.meta['proxy'] = 'https://' + ip
        else:
            ip = random.choice(PROXY_http)
            request.meta['proxy'] = 'http://' + ip


class City58SpiderDownloaderMiddleware(object):
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None


    def process_response(self, request, response, spider):

        return response

