from itemadapter import ItemAdapter
import scrapy
from scrapy.pipelines.images import ImagesPipeline
from pymongo import MongoClient
import hashlib
from scrapy.utils.python import to_bytes
from pathlib import Path

class OgoPipeline:

    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.database = client.ogo_video

    def process_item(self, item, spider):
        items = {}
        items['name'] = item['name'].replace('\n','').replace('  ','')
        spec = {}
        for i in range(len(item['specifications_keys'])):
            spec.setdefault(item['specifications_keys'][i] , item['specifications_value'][i])
        items['specifications'] = spec
        try:
            items['price'] = int(item['price'].replace('\xa0','').replace('руб.',''))
            items['currency'] = item['price'].split('\xa0')[-1]
        except:
            items['price'] = None
        items['link'] = item['href']
        items['photos'] = item['photos']


        print()
        collection = self.database[spider.name]
        collection.insert_one(items)
        return item


class OgoPhotosPipeline(ImagesPipeline):
    def get_media_requests(self, item, info):
        self.item_name = item['href'].split('/')[-2]
        if item['photos']:
            for img in item['photos']:
                img = 'https://ogo1.ru' + img
                try:
                    yield scrapy.Request(img)
                except Exception as e:
                    print(e)


#def file_path(self, request, response=None, info=None):
    #image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
    #return f'{self.crawler.spider.search_string}/{self.goods_name}/full/{image_guid}.jpg'

    def item_completed(self, results, item, info):
        if results:
            item['photos'] = [i[1] for i in results if i[0]]
        return item

    def file_path(self, request, response=None, info=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f'{Path.cwd()}/images/{self.item_name}/full/{image_guid}.jpg'

    def thumb_path(self, request, thumb_id, response=None, info=None):
        image_guid = hashlib.sha1(to_bytes(request.url)).hexdigest()
        return f'{self.item_name}/%s/%s.jpg' % (thumb_id, image_guid)