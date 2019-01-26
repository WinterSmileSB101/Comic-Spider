# -*- coding: utf-8 -*-
import scrapy


class M57comicSpider(scrapy.Spider):
    name = 'M57Comic'
    allowed_domains = ['http://www.57mh.com/']
    start_urls = ['http://http://www.57mh.com//']

    def parse(self, response):
        pass
