from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.common.exceptions import TimeoutException, WebDriverException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from pprint import pprint
from datetime import datetime, date, time
from pymongo import MongoClient




def mail_messages_scrapper(mongo_database_name, database_collection):
    chrome_options = Options()
    chrome_options.add_argument('start-maximized')
    main_link = 'https://mail.ru'
    driver = webdriver.Chrome("./chromedriver.exe", options=chrome_options)

    try:
        driver.get(main_link)
    except WebDriverException:
        print('Нет соединения с сайтом')
        return 0

    try:
        elem = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'mailbox:login-input')))
    except TimeoutException:
        print('Не прогружаются элементы страницы')
        return 0, driver
    elem.send_keys('study.ai_172')
    elem.submit()

    try:
        elem = WebDriverWait(driver, 5).until(EC.element_to_be_clickable((By.ID, 'mailbox:password-input')))
    except TimeoutException:
        print('Не прогружаются элементы страницы')
        return 0, driver
    elem.send_keys('NextPassword172')
    elem.submit()

    try:
        WebDriverWait(driver,20).until(EC.title_contains('Входящие'))
    except:
        print('Не прогружаются элементы страницы')
        return 0, driver

    last_link = None
    links_list = []
    while True:
        links = driver.find_elements_by_xpath("//div[@class='llc__background'][1]/..")
        pointer = links[-1]

        for i in range(len(links)):
            links[i] = links[i].get_attribute('href')

        if links[-1] == last_link:
            break

        for i in links_list:
            try:
                links.remove(i)
            except:
                continue

        links_list.extend(links)

        move = ActionChains(driver)
        move.move_to_element(pointer)
        move.perform()

        last_link = links[-1]
    messages_data = []
    for link in links_list:
        driver.get(link)
        messages_info = {}
        try:
            elem = WebDriverWait(driver, 5).until(EC.presence_of_element_located((By.TAG_NAME, 'h2')))
        except:
            return 0, driver


        messages_info['header'] = elem.text
        messages_info['sender'] = driver.find_element_by_xpath("//div[@class='letter__author']").text
        primary_date = driver.find_element_by_xpath("//div[@class='letter__date']").text
        now = datetime.now()
        if 'Вчера' in primary_date:
            date = (f'{primary_date}, {str(now.day - 1)}.{str(now.month)}.{str(now.year)}')
        elif 'Сегодня' in primary_date:
            date = (f'{primary_date}, {str(now.day)}.{str(now.month)}.{str(now.year)}')
        else:
            date = (f'{primary_date}')
        messages_info['date'] = date
        messages_info['text'] = driver.find_element_by_xpath("//div[@class='letter-body__body']").text
        messages_data.append(messages_info)

    client = MongoClient('127.0.0.1', 27017)
    db = client[mongo_database_name]
    writer = db[database_collection]
    db_data = list(writer.find({},{'header' : True, '_id' : False}))
    data_list = [data['header'] for data in db_data]
    counter = 0
    for message in messages_data:
        if message['header'] not in data_list:
            writer.insert_one(message)
            counter += 1
    print(f'Добавлено новых сообщений: {counter}')


mail_messages_scrapper('mail_base', 'study_ai')


