from scrapy.crawler import CrawlerProcess
from scrapy.settings import Settings
from ogo import settings
from ogo.spiders.ogo_ru import OgoRuSpider

if __name__ == '__main__':
    my_settings = Settings()
    my_settings.setmodule(settings)
    #u_search = input('Введите запрос: ')
    proc = CrawlerProcess(settings=my_settings)
    proc.crawl(OgoRuSpider, search = 'видеокарта')

    proc.start()
