import scrapy
from amazon_scraper.items import AmazonBookItem
import re
from scrapy.spidermiddlewares.httperror import HttpError
from twisted.internet.error import DNSLookupError
from twisted.internet.error import TimeoutError, TCPTimedOutError
from amazon_scraper.amazon_scraper_logger import amazon_scraper_logger as logger


class AmazonSpider(scrapy.Spider):
    name = 'amazon_ebooks'
    base_url = "https://www.amazon.com"
    start_urls = ['https://www.amazon.com/s?k=best+selling+books&i=stripbooks-intl-ship&ref=nb_sb_noss']

    def parse(self, response):
        logger.info('AmazonSpider parse method got successful response from  {}'.format(response.url))
        section_div_list = response.xpath("//div[@class='a-section a-spacing-medium']/div[2]")
        for div in section_div_list:
            item = AmazonBookItem()
            img_src = div.css("img[class='s-image']::attr(src)").get()
            title_author_div = div.xpath('div[2]/div/div[1]/div/div')
            title = title_author_div.xpath("div[1]/h2/a/span/text()").get()
            published_date_xpath = """div[1]/div/span[@class='a-size-base a-color-secondary a-text-normal']/text()"""
            published_date = title_author_div.xpath(published_date_xpath).get()
            try:
                author = title_author_div.xpath("div[1]/div").css('::text').extract()
                author_clean = ''.join([obj.strip() for obj in author if obj.strip() not in ['', '|']][1:-1])
            except (ValueError, IndexError) as e:
                logger.error('Error in AmazonSpider parse while fetching author field: {}'.format(str(e)))
                author_clean = None
            reviews = title_author_div.xpath("div[2]/div/span[2]/a/span/text()").get()
            ratings_str = title_author_div.xpath("div[2]/div/span[1]").css('::attr(aria-label)').get()
            # rating_rgx = re.compile("(\d.\d|\d)")
            if ratings_str:
                res = re.findall(r"(\d.\d|\d)", ratings_str)
                if res:
                    ratings = res[0]
                else:
                    ratings = None
            else:
                ratings = None
            item['image'] = img_src
            item['title'] = title
            item['published_date'] = published_date
            item['author'] = author_clean
            item['reviews'] = reviews
            item['ratings'] = ratings

            detail_link_href = self.base_url + div.xpath('div[1]/div/div/span/a').css('::attr(href)').get()
            request = scrapy.Request(detail_link_href, callback=self.parse_detail_page, cb_kwargs={'item': item})
            yield request
        next_page_xpath = "//span[@cel_widget_id='MAIN-PAGINATION']/div/div/ul/li[@class='a-last']/a/@href"
        next_page_link = response.xpath(next_page_xpath).get()
        logger.info('AmazonSpider parse next page link. {}'.format(next_page_link))
        if next_page_link:
            absolute_next_page_url = self.base_url + next_page_link
            yield scrapy.Request(absolute_next_page_url)

    def parse_detail_page(self, response, item):
        logger.info('AmazonSpider parse_detail_page method got successful response from  {}'.format(response.url))
        li_list = response.xpath("//div[@id='tmmSwatches']/ul/li")
        book_type_price_dict = {}
        for li in li_list:
            try:
                book_type_text_list = li.xpath('span/span/span/a/span').css('::text').extract()
                book_type = [obj.strip() for obj in book_type_text_list if obj.strip() not in ['', '\n']][0]
                price_str = li.xpath('span/span/span/a/span[2]/span/text()').get()
                price_stripped = price_str.strip() if price_str else price_str
                book_type_price_dict[book_type] = price_stripped
            except (ValueError, IndexError) as e:
                logger.error('Error in AmazonSpider parse_detail_page. {}'.format(str(e)))
        item['book_type_price'] = book_type_price_dict
        return item

    def errback_httpbin(self, failure):
        # log all failures
        logger.error(repr(failure))

        # in case you want to do something special for some errors,
        # you may need the failure's type:

        if failure.check(HttpError):
            # these exceptions come from HttpError spider middleware
            # you can get the non-200 response
            response = failure.value.response
            logger.error('AmazonSpider HttpError on %s', response.url)

        elif failure.check(DNSLookupError):
            # this is the original request
            request = failure.request
            logger.error('AmazonSpider DNSLookupError on %s', request.url)

        elif failure.check(TimeoutError, TCPTimedOutError):
            request = failure.request
            logger.error('AmazonSpider TimeoutError on %s', request.url)
