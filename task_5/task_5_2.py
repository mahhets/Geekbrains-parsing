from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
import time


def mvideo_scrapper(mongo_database_name, database_collection):
    chrome_options = Options()
    chrome_options.add_argument('start-maximized')
    main_link = 'https://www.mvideo.ru/'
    driver = webdriver.Chrome("./chromedriver.exe", options=chrome_options)

    try:
        driver.get(main_link)
    except WebDriverException:
        print('Нет соединения с сайтом')
        return 0, driver

    try:
        WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.CLASS_NAME, 'manufacturers-list-wrap')))
    except TimeoutException:
        print('Не прогружаются элементы страницы')
        return 0, driver

    positions = driver.find_elements_by_xpath('//div[contains(@class,"h2")]')
    position_number = 0
    for position in range(len(positions)):
        if 'Хиты продаж' in positions[position].text:
            position_number = position
            break

    sliders = driver.find_elements_by_xpath("//ul[contains(@data-init,'galleryCarousel')]")
    products_data = []
    while True:
        products = sliders[position_number].find_elements_by_xpath("./li/div")
        time.sleep(2)
        for i in range(4):
            products_info = {}

            products_info['name'] = products[i].find_element_by_xpath(".//h4").get_attribute('title')
            product_price = products[i].find_element_by_xpath(".//div[contains(@data-sel,'div-price_current')]").text
            products_info['price'] = product_price.replace(' ','')

            products_data.append(products_info)


        next_products_slide = sliders[position_number].find_element_by_xpath("./../../a[contains(@class,'next-btn')]")
        next_products_slide.click()
        if 'disabled' in next_products_slide.get_attribute('class'):
            break

    client = MongoClient('127.0.0.1', 27017)
    db = client[mongo_database_name]
    writer = db[database_collection]
    db_data = list(writer.find({}, {'name': True, '_id': False}))
    data_list = [data['name'] for data in db_data]
    counter = 0
    for message in products_data:
        if message['name'] not in data_list:
            writer.insert_one(message)
            counter += 1
    print(f'Добавлено новых товаров: {counter}')


mvideo_scrapper('products', 'sales_hits')