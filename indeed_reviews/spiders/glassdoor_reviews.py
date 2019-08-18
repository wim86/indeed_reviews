
from scrapy.spiders import Spider
from scrapy import Request

from indeed_reviews.items import IndeedReviewsItem, IndeedReviewsItemLoader
from urllib.parse import urlencode
from itertools import islice


class GlassdoorSpider(Spider):
    name = 'glassdoor'

    allowed_domains = ['glassdoor.com', ]
    start_urls = ['https://www.glassdoor.com/Reviews/index.htm']
    maximum_reviews = 20

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse(self, response):
        company_name = response.meta['company_name']
        search_url = 'https://www.glassdoor.com/Reviews/company-reviews.htm?'
        query = {'suggestCount': 0,
                 'suggestChosen': 'false',
                 'clickSource': 'searchBtn',
                 'typedKeyword': company_name,
                 'sc.keyword': company_name,
                 'locT': '',
                 'locId': '',
                 'jobType': ''
                 }

        yield Request(search_url + urlencode(query),
                      callback=self.parse_search)

    def parse_search(self, response):
        reviews_url = response.xpath(
                '//*[contains(@class, "empLinks")]'
                '//*[contains(@class, "reviews")]/@href'
        ).extract_first()
        yield Request(response.urljoin(reviews_url),
                      callback=self.parse_reviews)

    def parse_reviews(self, response):
        total_reviews = response.meta.get('number_reviews', 0)
        reviews_xpath = response.xpath('//*[starts-with(@class,"empReview")]')
        for review_xpath in islice(
                        reviews_xpath, 0, self.maximum_reviews - total_reviews):
            loader = IndeedReviewsItemLoader(
                item=IndeedReviewsItem(), response=response)
            title = review_xpath.xpath(
                './/*[@class="summary"]/text()'
            ).extract_first()
            stars = review_xpath.xpath(
                './/*[@class="value-title"]/text()'
            ).extract_first()
            division = review_xpath.xpath(
                './/*[@class="authorInfo"]/span/text()'
            ).extract_first()
            location = review_xpath.xpath(
                './/*[@class="authorLocation"]/text()'
            ).extract_first()
            date = review_xpath.xpath(
                './/*[starts-with(@class,"date")]/text()'
            ).extract_first()
            review = review_xpath.xpath(
                './/*[starts-with(@class, "mainText")]/text()'
            ).extract()
            pros = review_xpath.xpath(
                './/*[@class="strong"][text() = "Pros"]'
                '/following-sibling::p/text()'
            ).extract_first()
            cons = review_xpath.xpath(
                './/*[@class="strong"][text() = "Cons"]'
                '/following-sibling::p/text()'
            ).extract_first()

            loader.add_value('title', title)
            loader.add_value('stars', stars)
            loader.add_value('division', division)
            loader.add_value('location', location)
            loader.add_value('date', date)
            loader.add_value('review', review)
            loader.add_value('pros', pros)
            loader.add_value('cons', cons)
            item = loader.load_item()
            yield item

        if (len(reviews_xpath) + total_reviews) < self.maximum_reviews:
            total_reviews = total_reviews + len(reviews_xpath)
            next_page = response.xpath(
                '//*[contains(@class, "nextArrow")]/@href'
            ).extract_first()
            yield Request(response.urljoin(next_page),
                          callback=self.parse_reviews,
                          meta={'number_reviews': total_reviews})
