
from scrapy.spiders import Spider
from scrapy import Request

from indeed_reviews.items import IndeedReviewsItem, IndeedReviewsItemLoader
from urllib.parse import urlencode
from itertools import islice


class IndeedSpider(Spider):
    name = 'indeed'

    allowed_domains = ['indeed.co.uk', ]
    start_urls = ['https://www.indeed.co.uk/companies']
    maximum_reviews = 20

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def parse(self, response):
        company_name = response.meta['company_name']
        search_url = 'https://www.indeed.co.uk/cmp?'
        query = {'from': 'discovery-cmp-front-door',
                 'q': company_name}

        yield Request(search_url + urlencode(query),
                      callback=self.parse_search)

    def parse_search(self, response):
        company_url = response.xpath(
            '//*[@itemprop="url"]/@href'
        ).extract_first()
        yield Request(response.urljoin(company_url) + '/reviews',
                      callback=self.parse_reviews)

    def parse_reviews(self, response):
        reviews_xpath = response.xpath('//*[@class="cmp-review"]')
        for review_xpath in islice(reviews_xpath, 0, self.maximum_reviews):
            loader = IndeedReviewsItemLoader(
                item=IndeedReviewsItem(), response=response)
            title = review_xpath.xpath(
                './/*[@class="cmp-review-title"]/span/text()'
            ).extract_first()
            stars = review_xpath.xpath(
                './/*[@class="cmp-ratingNumber"]/text()'
            ).extract_first()
            division = review_xpath.xpath(
                './/*[@itemprop="author"]/*[@itemprop="name"]/@content'
            ).extract_first()
            location = review_xpath.xpath(
                './/*[@class="cmp-reviewer-job-location"]/text()'
            ).extract_first()
            date = review_xpath.xpath(
                './/*[@class="cmp-review-date-created"]/text()'
            ).extract_first()
            review = review_xpath.xpath(
                './/*[@itemprop="reviewBody"]/text()'
            ).extract()
            pros = review_xpath.xpath(
                './/*[@class="cmp-review-pro-text"]/text()'
            ).extract_first()
            cons = review_xpath.xpath(
                './/*[@class="cmp-review-con-text"]/text()'
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
