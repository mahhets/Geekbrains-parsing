from pprint import pprint
from lxml import html
import requests
from datetime import datetime, date, time
from pymongo import MongoClient

class MainNewsScrapper:
    def LentaNewsScrapper(self):
        lental = 'https://lenta.ru'
        header = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.86'}
        rep = requests.get(lental, headers = header)
        dom = html.fromstring(rep.text)
        news = dom.xpath("//section[contains(@class, 'js-top-seven')]/div//div[contains(@class, 'item')]")
        lenta = []
        for new in news:
            lenta_news = {}
            sourse = 'lenta.ru'
            name = str(new.xpath(".//a/text()")[0])
            href = new.xpath(".//a/@href")[0]
            time = new.xpath(".//a//@datetime")[0]
            lenta_news['name'] = name.replace('\xa0',' ')
            lenta_news['link'] = lental +  href
            lenta_news['time'] = time
            lenta_news['sourse'] = sourse
            lenta.append(lenta_news)
        return lenta


    def YandexNewsScrapper(self):
        yandexl = 'https://yandex.ru/news'
        header = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.86'}
        rep = requests.get(yandexl, headers=header)
        dom = html.fromstring(rep.text)
        news = dom.xpath("//div[contains(@class, 'news-top-stories')]/div")
        yandex = []
        for new in news:
            now = datetime.now()
            yandex_news = {}
            name = new.xpath(".//h2/text()")[0]
            test_link = new.xpath(".//div[@class='news-card__inner']/a/@href")
            if test_link:
                href = new.xpath(".//div[@class='news-card__inner']/a/@href")[0]
            else:
                href = new.xpath("./article/a/@href")[0]
            sourse = new.xpath(".//span[@class='mg-card-source__source']/a/text()")[0]
            test_time = new.xpath(".//span[@class='mg-card-source__time']/text()")[0]
            if 'вчера' in test_time:
                time = (f'{test_time}, {str(now.day - 1)}.{str(now.month)}.{str(now.year)}')
            else:
                time = (f'{test_time}, {str(now.day)}.{str(now.month)}.{now.year}')
            yandex_news['name'] = name
            yandex_news['link'] = href
            yandex_news['time'] = time
            yandex_news['sourse'] = sourse
            yandex.append(yandex_news)
        return yandex

    def MailNewsScrapper(self):
        maill = 'https://news.mail.ru'
        header = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.86'}
        rep = requests.get(maill, headers=header)
        dom = html.fromstring(rep.text)
        news = dom.xpath("//div[@class='js-module']//div[contains(@class, 'daynews__item')]")
        mail = []
        for new in news:
            mail_news = {}
            name = new.xpath(".//span[contains(@class,'photo__title')]/text()")[0]
            href = new.xpath(".//a/@href")[0]
            news_link = requests.get(href, headers=header)
            news_dom = html.fromstring(news_link.text)
            sourse = news_dom.xpath("//span[@class='breadcrumbs__item']//span[@class='link__text']/text()")[0]
            time = str(news_dom.xpath("//span[@class='breadcrumbs__item']/span/span/@datetime")[0])
            mail_news['name'] = name.replace('\xa0', ' ')
            mail_news['link'] = href
            mail_news['sourse'] = sourse
            mail_news['time'] = time.replace('T', ' ')
            mail.append(mail_news)
        return mail


def news_mongo_writer(database,collection):
    client = MongoClient('127.0.0.1', 27017)
    db = client[database]
    news = db[collection]
    all_news = MainNewsScrapper.YandexNewsScrapper(1) \
                + MainNewsScrapper.LentaNewsScrapper(1) \
                + MainNewsScrapper.MailNewsScrapper(1)
    news.insert_many(all_news)



# ----- Запись в БД
# Хотел сделать коллекции как datetime, но mongo против)

news_mongo_writer('news_bd', 'day_1')


