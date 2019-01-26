# -*- coding: utf-8 -*-
import scrapy


class M98comicSpider(scrapy.Spider):
    name = 'M98Comic'
    allowed_domains = ['http://www.98comic.com/']
    start_urls = ['http://www.98comic.com/list']

    def start_requests(self):
        urls = [
        'http://www.98comic.com/list'
        ]
        for url in urls:
            yield scrapy.Request(url=url,callback=self.parse)

    def parse(self, response):
        title = response.css('.book-list>#contList>.bgcover::title').extract_first();
        print(title);
        print("执行完了")