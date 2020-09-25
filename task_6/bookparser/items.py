# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class BookparserItem(scrapy.Item):
    book_name = scrapy.Field()
    author = scrapy.Field()
    old_price = scrapy.Field()
    new_price = scrapy.Field()
    rating = scrapy.Field()
    book_link = scrapy.Field()
    currency = scrapy.Field()

