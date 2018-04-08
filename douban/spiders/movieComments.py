# -*- coding: utf-8 -*-
import scrapy
from douban.items import DoubanCommet
import sys
#print(sys.getdefaultencoding())
#reload(sys)
#sys.setdefaultencoding('utf-8')

class MoviecommentsSpider(scrapy.Spider):
    name = 'movieComments'
    allowed_domains = ['movie.douban.com']
    start_urls = ['https://movie.douban.com/subject/3445906/comments?sort=time&status=P']

    # def __init__(self):
    #     f = open('MovieList.txt', 'r')
    #     allLines = f.read()
    #     lines = allLines.split('\n')
    #     f.close()
    #     self.start_urls=[]
    #     for line in lines:
    #         if (line !=  ''):
    #             url = 'https://movie.douban.com/subject/' + line + '/comments?status=P'
    #             self.start_urls.append(url)

    def parse(self, response):

        #response.encoding('utf-8')
        for comment in response.xpath('//div[@class="comment"]'):
            item = DoubanCommet()
            item['id'] = comment.xpath('./h3/span[@class="comment-info"]/a/@href').extract_first().split('/')[-2]
            item['rate'] = comment.xpath('./h3/span[@class="comment-info"]/span[@class]/@title').extract_first()
            item['comment'] = comment.xpath('./p[@class=""]/text()').extract_first().replace(' ', '').replace('\n', '')
            yield item

        url_base = response.xpath('//div[@class="aside"]/p/a/@href').extract_first()
        next_page_url = response.xpath('//a[@class="next"]/@href').extract_first()

        if next_page_url is not None:
            # print('########')
            # print(url_base)
            # print(next_page_url)
            url = url_base + 'comments' +next_page_url
            # url = url.encode('ascii')
            # print(type(url))
            # print(url)
            yield scrapy.Request(url)

