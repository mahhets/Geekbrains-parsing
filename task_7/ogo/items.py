# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class OgoItem(scrapy.Item):
    _id = scrapy.Field()
    name = scrapy.Field()
    specifications_keys = scrapy.Field()
    specifications_value = scrapy.Field()
    price = scrapy.Field()
    href = scrapy.Field()
    photos = scrapy.Field()
    currency = scrapy.Field()

