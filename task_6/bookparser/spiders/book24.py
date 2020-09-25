import scrapy
from scrapy.http import HtmlResponse
from bookparser.items import BookparserItem


class Book24Spider(scrapy.Spider):
    name = 'book24'
    allowed_domains = ['book24.ru']
    start_urls = ['https://book24.ru/catalog/fantastika-1649']

    def parse(self, response:HtmlResponse):
        book_links = response.css("a.book__image-link::attr(href)").extract()
        for link in book_links:
            yield response.follow(link, callback=self.data_scrapper)

        next_page = response.xpath(
            '//a[contains(@class,"catalog-pagination__item _text js-pagination-catalog-item")][text()="Далее"]'
            '/@href').extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        print()


    def data_scrapper(self, response:HtmlResponse):
        book_name = response.xpath('//h1/text()').extract_first()
        author = response.xpath("//div[@class='item-tab__chars-item'][1]/span[2]/a/text()").extract_first()

        old_price = response.xpath('//div[@class="item-actions__price-old"]/text()').extract_first()
        if not old_price:
            old_price = response.xpath('//div[@class="item-actions__price"]/b/text()').extract_first()
            new_price = None
        else:
            old_price = None
            new_price = response.xpath('//div[@class="item-actions__price"]/b/text()').extract_first()

        currency = response.css("div.item-actions__price::text").extract_first()
        rating = response.css("span.rating__rate-value::text").extract_first()
        if not rating:
            rating = '0'
        book_link = response.url

        yield BookparserItem(book_name=book_name, author=author, old_price=old_price,
                             new_price=new_price, rating=rating,book_link=book_link, currency=currency)


