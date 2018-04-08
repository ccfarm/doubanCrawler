# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import codecs
import scrapy
from douban.items import Movie
from douban.items import Review

class DoubanPipeline(object):
    # def __init__(self):
    #     self.f = codecs.open('test.txt', 'w', 'utf-8')

    def process_item(self, item, spider):
        if isinstance(item, Review):
            filename = 'data/%s/%s.txt'%(item['id'],item['review_id'])
            # print('#########' + filename)
            f = codecs.open(filename,'w', 'utf-8')
            f.write(item['name'] + u'\n')
            f.write(item['rate'] + u'\n')
            f.write(item['time'] + u'\n')
            f.write(item['title'] + u'\n')
            f.write(item['content'])
            f.close()
        elif isinstance(item, Movie):
            filename = 'data/%s/info.txt' % item['id']
            f = codecs.open(filename, 'w', 'utf-8')
            f.write(item['name'] + u'\n')
            f.write(item['year'] + u'\n')
            for a in item['director']:
                f.write(a + u'/')
            f.write(u'\n')
            for a in item['writer']:
                f.write(a + u'/')
            f.write(u'\n')
            for a in item['actor']:
                f.write(a + u'/')
            f.write(u'\n')
            for a in item['genre']:
                f.write(a + u'/')
            f.write(u'\n')
            f.write(item['date'] +u'\n')
            f.write(item['rate'] + u'\n')
            f.write(item['rating_people'] + u'\n')
            f.write(item['name'] + u'\n')
            for a in item['tag']:
                f.write(a + u'/')
            f.write(u'\n')
            f.write(item['comment'] + u'\n')
            f.write(item['summary'])
            f.close()
        return item
