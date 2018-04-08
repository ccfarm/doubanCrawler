# -*- coding: utf-8 -*-
import scrapy
import json


class CrawmovielistSpider(scrapy.Spider):
    name = 'crawMovieList'
    allowed_domains = ['movie.douban.com']

    def __init__(self):
        self.f = open('chineseMovieList.txt', 'a')
        self.start = 0
        self.baseUrl= 'https://movie.douban.com/j/new_search_subjects?sort=R&range=0,10&tags=%E5%A4%A7%E9%99%86,%E7%94%B5%E5%BD%B1&start='
        self.start_urls = [self.baseUrl + str(self.start)]

    def parse(self, response):
        j = json.loads(response.body)
        for dic in j['data']:
            self.f.write(dic['url'] + '\n')
        while self.start < 3500:
            self.start = self.start + 20
            yield scrapy.Request(self.baseUrl + str(self.start))


