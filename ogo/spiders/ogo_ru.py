import scrapy
from scrapy.http import HtmlResponse
from ogo.items import OgoItem



class OgoRuSpider(scrapy.Spider):
    name = 'ogo_ru'
    allowed_domains = ['ogo1.ru']

    def __init__(self, search):
        self.start_urls = [f'https://ogo1.ru/search/?only_available=1&query={search}']

    def parse(self, response:HtmlResponse):
        links_list = response.xpath("//a[contains(@class,'url setSampleId')]")
        for link in links_list:
            yield response.follow(link,  callback=self.link_pars)

        next_page = 'https://ogo1.ru' + response.xpath(
            "//a[contains(@class,'page_nav_next page_nav_next_big icon ')]/@href").extract_first()
        if next_page:
            yield response.follow(next_page, callback=self.parse)

    def link_pars(self, response:HtmlResponse):
        name = response.css("h1::text").extract_first()
        specifications_keys = response.xpath("//td[@class='col1']/text() | "
                                        "//td[@class='g-product-params__param-label']/text()").extract()
        specifications_value = response.xpath("//tr/td[contains(@class, 'black col2')]/text() | "
                                              "//td[@class='g-product-params__param-value']/text()").extract()
        price = response.xpath("//div[contains(@class,'price clearfix')]/div/text()").extract_first()
        href = response.url
        photos = response.xpath("//li[@class='button ']/img/@data-src | //li[contains(@class,'button active')]/img/@data-src").extract()
        yield OgoItem(name=name, specifications_keys=specifications_keys,specifications_value=specifications_value,
                      price=price, href=href, photos=photos)
