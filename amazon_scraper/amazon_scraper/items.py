# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class AmazonBookItem(scrapy.Item):
    # define the fields for your item here like:
    title = scrapy.Field()
    author = scrapy.Field()
    image = scrapy.Field()
    published_date = scrapy.Field()
    reviews = scrapy.Field()
    book_price = scrapy.Field()
    ratings = scrapy.Field()
    book_type_price = scrapy.Field()
