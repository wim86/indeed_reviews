# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader.processors import TakeFirst, Identity, Compose, MapCompose, \
    Join


def compact(string):
    """ returns None if string is empty, otherwise string itself """
    return string if string else None


class IndeedReviewsItemLoader(scrapy.loader.ItemLoader):
    """ Class containing the ItemLoader for clothes"""
    # default input & output processors
    # will be executed for each item loaded,
    # except if a specific in or output processor is specified
    default_input_processor = Identity()
    default_output_processor = TakeFirst()

    review_in = Compose(MapCompose(str.strip, compact),
                             Join())


class IndeedReviewsItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    title = scrapy.Field()
    stars = scrapy.Field()
    division = scrapy.Field()
    location = scrapy.Field()
    date = scrapy.Field()
    review = scrapy.Field()
    pros = scrapy.Field()
    cons = scrapy.Field()
    pass
