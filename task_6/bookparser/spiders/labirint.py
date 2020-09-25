import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class LabirintSpider(scrapy.Spider):
    name = 'labirint_ru'
    allowed_domains = ['labirint.ru']
    start_urls = ['https://www.labirint.ru/search/%D1%84%D0%B0%D0%BD%D1%82%D0%B0%D1%81%D1%82%D0%B8%D0%BA%D0%B0/?stype=0&page=1']

    def parse(self, response: HtmlResponse):
        book_links = response.xpath('//a[@class="cover"]/@href').extract()
        for link in book_links:
            yield response.follow(link, callback=self.data_scrapper)

        next_page = response.xpath('//a[@class="pagination-next__text"]/@href').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def data_scrapper(self, response: HtmlResponse):
        book_name = response.css("h1::text").extract_first()

        old_price = None
        new_price = None
        price = response.xpath('//div[@class="buying"]//text()').extract()
        if 'Нет в продаже' not in price:
            if 'Цена для всех' in price:
                old_price = response.xpath('//span[@class="buying-priceold-val-number"]/text()').extract_first()
                new_price = response.xpath('//span[@class="buying-pricenew-val-number"]/text()').extract_first()
            else:
                old_price = response.xpath('//span[@class="buying-price-val-number"]/text()').extract_first()

        rating = response.xpath('//div[@id="rate"]/text()').extract_first()
        book_link = response.url
        currency = response.css('span.buying-pricenew-val-currency::text').extract_first()


        yield BookparserItem(book_name=book_name, book_link=book_link, old_price=old_price,
                             new_price=new_price, rating=rating, currency=currency)