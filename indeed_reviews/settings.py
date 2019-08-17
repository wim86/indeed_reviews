# -*- coding: utf-8 -*-

# Scrapy settings for indeed_reviews project
#
# For simplicity, this file contains only settings considered important or
# commonly used. You can find more settings consulting the documentation:
#
#     https://docs.scrapy.org/en/latest/topics/settings.html
#     https://docs.scrapy.org/en/latest/topics/downloader-middleware.html
#     https://docs.scrapy.org/en/latest/topics/spider-middleware.html

BOT_NAME = 'indeed_reviews'

SPIDER_MODULES = ['indeed_reviews.spiders']
NEWSPIDER_MODULE = 'indeed_reviews.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True
