

from scrapy.spiders import Spider
from scrapy import Request

from urllib.parse import urlencode, urljoin
import logging


class IndeedSpider(Spider):
    name = 'indeed'

    allowed_domains = ['indeed.co.uk', ]
    start_urls = ['https://www.indeed.co.uk/companies']

    def __init__(self, company_name, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.company_name = company_name
        logging.debug(f"company name is {company_name}")

    def parse(self, response):
        logging.debug(f"start parse for url: {response.url}")
        search_url = 'https://www.indeed.co.uk/cmp?'
        query = {'from': 'discovery-cmp-front-door',
                 'q': self.company_name}

        yield Request(search_url + urlencode(query),
                      callback=self.parse_search)

    def parse_search(self, response):
        logging.debug(f"parse_search for {response.url}")
        company_url = response.xpath(
            '//*[@itemprop="url"]/@href'
        ).extract_first()
        logging.debug(f"company_url is {company_url}")
        yield Request(response.urljoin(company_url) + '/reviews',
                      callback=self.parse_reviews)

    def parse_reviews(self, response):
        logging.debug(f"parse_reviews for {response.url}")
        from scrapy.shell import inspect_response
        inspect_response(response, self)
