# -*- coding: utf-8 -*-
import scrapy
from douban.items import Movie
from douban.items import Review
import os
from bs4 import BeautifulSoup


class MovieSpider(scrapy.Spider):
    name = 'movie1'
    allowed_domains = ['movie.douban.com']
    start_urls = []

    def __init__(self):

        f = open('doneList.txt', 'r')
        allLines = f.read()
        lines = allLines.split('\n')
        self.s = set(lines)
        f.close()

        f = open('todolist.txt', 'r')
        allLines = f.read()
        lines = allLines.split('\n')
        f.close()

        for line in lines:
            if (line !=  '') and (not line in self.s):
                self.start_urls.append(line)

    def parse(self, response):
        self.base_url = response.url
        if response.status == 403:
            exit(403)
        # print('#####' + response.status)
        # print(type(response.status))
        dir = 'data/' + response.url.split('/')[-2]
        if not os.path.isdir(dir):
            os.mkdir(dir)
        item = Movie()
        item['id'] = response.url.split('/')[-2]
        item['name'] = response.xpath('//span[@property="v:itemreviewed"]/text()').extract_first()
        item['year'] = response.xpath('//span[@class="year"]/text()').extract_first().replace('(', '').replace(')','')
        info = response.xpath('//div[@id="info"]')
        list = []
        for a in info.xpath('./span[1]/span[2]/a'):
            list.append(a.xpath('./text()').extract_first())
        item['director'] = list
        list = []
        for a in info.xpath('./span[2]/span[2]/a'):
            list.append(a.xpath('./text()').extract_first())
        item['writer'] = list
        list = []
        for a in info.xpath('//a[@rel="v:starring"]'):
            list.append(a.xpath('./text()').extract_first())
        item['actor'] = list
        list = []
        for a in response.xpath('//span[@property="v:genre"]'):
            list.append(a.xpath('./text()').extract_first())
        item['genre'] = list
        item['date'] = info.xpath('//span[@property="v:initialReleaseDate"]/text()').extract_first()
        item['rate'] = response.xpath('//strong[@property="v:average"]/text()').extract_first()
        item['rating_people'] = response.xpath('//span[@property="v:votes"]/text()').extract_first()
        list = []
        for a in response.xpath('//div[@class="tags-body"]/a'):
            list.append(a.xpath('./text()').extract_first())
        item['tag'] = list
        item['comment'] = info.xpath('//a[@href = "reviews"]/text()').extract_first()
        item['summary'] = info.xpath('//span[@property="v:summary"]/text()').extract_first().replace(u'\n', u'').replace(u' ', u'').replace(u'\u3000',u'')
        print(type(item))
        yield item
        yield scrapy.Request(self.base_url + 'reviews', self.parse_review_list)

    def parse_review_list(self, response):
        for url in response.xpath('//div[@class="main-bd"]/h2/a/@href').extract():
            id = self.base_url.split('/')[-2]
            review_id = url.split('/')[-2]
            if  not os.path.exists('data/%s/%s.txt'%(id, review_id)):
                yield scrapy.Request(url, self.parse_review)
        next = response.xpath('//link[@rel="next"]/@href').extract_first()
        # print('####' + next)
        # print(self.base_url + 'reviews' + next)
        if next == None:
            f = open('doneList.txt', 'a')
            f.write(self.base_url + '\n')
            f.close()
        else:
            yield scrapy.Request(self.base_url + 'reviews' + next, self.parse_review_list)


    def parse_review(self, response):
        item = Review()
        item['review_id'] = response.url.split('/')[-2]
        item['id'] = response.xpath('//div[@class ="subject-title"]/a/@href').extract_first().split('/')[-2]
        item['name'] = response.xpath('//span[@property="v:reviewer"]/text()').extract_first()
        item['rate'] = response.xpath('//span[@property="v:rating"]/text()').extract_first()
        item['time'] = response.xpath('//span[@property="v:dtreviewed"]/text()').extract_first()
        item['title'] = response.xpath('//span[@property="v:summary"]/text()').extract_first()
        soup = BeautifulSoup(response.text)
        content = soup.find(property="v:description")
        item['content'] = content.get_text().replace(u'\n', '')
        # list = []
        # for p in content.children:
        #     print(p)
        #     print(type(p))
        #     list.append(p.string)
        # item['content'] = '\n'.join(list)
        # item['content'] = '\n'.join(response.xpath('//div[@property="v:description"]/p/text()').extract())
        return item