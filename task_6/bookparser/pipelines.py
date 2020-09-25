# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
from pprint import pprint

class BookparserPipeline:
    counter = {"book24" : 0, "labirint" : 0}
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.database = client['books']

    def process_item(self, item, spider):
        book = {}
        if ":" in item['book_name']:
            header = item['book_name'].split(":")
            book['name'] = header[1]
            book['author'] = header[0]
        else:
            book['name'] = item['book_name']
            book['author'] = item['author']

        book['link'] = item['book_link']
        book['rating'] = float(item['rating'].replace(',','.'))
        if not book['rating']:
            book['rating'] = None
        book['old_price'] = item['old_price']
        if not book['old_price']:
            book['old_price'] = None
        else:
            book['old_price'] = int(item['old_price'])

        book['new_price'] = item['new_price']
        if not book['new_price']:
            book['new_price'] = None
        else:
            book['new_price'] = int(item['new_price'])
        book['currency'] = item['currency'].replace('.','')


        mongo = self.database[spider.name]
        mongo.insert_one(book)
        pprint(book)
        return item
