# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class IndeedReviewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    stars = scrapy.Field()
    division = scrapy.Field()
    location = scrapy.Field()
    date = scrapy.Field()
    review = scrapy.Field()
    pass
