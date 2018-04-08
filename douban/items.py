# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy

class Movie(scrapy.Item):
    id = scrapy.Field()
    name = scrapy.Field()
    year = scrapy.Field()
    director = scrapy.Field()
    actor = scrapy.Field()
    writer = scrapy.Field()
    date = scrapy.Field()
    genre = scrapy.Field()
    rate = scrapy.Field()
    rating_people = scrapy.Field()
    tag = scrapy.Field()
    comment = scrapy.Field()
    summary = scrapy.Field()

class Review(scrapy.Item):
    review_id = scrapy.Field()
    id = scrapy.Field()
    name = scrapy.Field()
    rate = scrapy.Field()
    time = scrapy.Field()
    title = scrapy.Field()
    content = scrapy.Field()

class DoubanCommet(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    id = scrapy.Field()
    rate = scrapy.Field()
    comment = scrapy.Field()