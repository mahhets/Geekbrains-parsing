import requests
from bs4 import BeautifulSoup as bs
import re
import pandas as pd
from pprint import pprint
ml = 'https://hh.ru/vacancies/'
headers = {'User-Agent' : 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/84.0.4147.86'}
super_link = 'https://www.superjob.ru'
sl = 'https://www.superjob.ru/vakansii/farmacevt.html'


jobs = []
page = 0
while True:
    params = {'page': page}
    job = 'farmacevt'
    html = requests.get(ml + job, params=params, headers=headers)
    soup = bs(html.text, 'html.parser')

    vacancy_blok = soup.find('div', {'class': 'vacancy-serp'})
    vacancy_list = vacancy_blok.find_all('div', {'class': 'vacancy-serp-item'})
    vacancy_button = soup.find('a', {'class': 'bloko-button HH-Pager-Controls-Next HH-Pager-Control'})

    for vacancy in vacancy_list:
        vacancy_data = {}
        vacancy_name = vacancy.find('a',{'class' : 'bloko-link HH-LinkModifier'}).getText()
        vacancy_link = vacancy.find('a',{'class' : 'bloko-link HH-LinkModifier'})['href']
        vacancy_salary = vacancy.find('div', {'class': 'vacancy-serp-item__sidebar'})
        if vacancy_salary:
            try:
                salary_all = vacancy.find('div', {'class': 'vacancy-serp-item__sidebar'}).getText()
                if 'до' in salary_all:
                    min_salary = None
                    salary_2 = re.findall(r'\d{2}.\d{3}', vacancy.find('div', {'class' : 'vacancy-serp-item__sidebar'}).getText())[0]
                    max_salary = float(salary_2.replace(u'\xa0', u''))
                elif 'от' in salary_all:
                    salary_1 = re.findall(r'\d{2}.\d{3}', vacancy.find('div', {'class' : 'vacancy-serp-item__sidebar'}).getText())[0]
                    min_salary = float(salary_1.replace(u'\xa0', u''))
                    max_salary = None
                else:
                    salary_1 = re.findall(r'\d{2}.\d{3}', vacancy.find('div', {'class': 'vacancy-serp-item__sidebar'}).getText())[0]
                    salary_2 = re.findall(r'\d{2}.\d{3}', vacancy.find('div', {'class': 'vacancy-serp-item__sidebar'}).getText())[1]
                    min_salary = float(salary_1.replace(u'\xa0', u''))
                    max_salary = float(salary_2.replace(u'\xa0', u''))

            except:
                min_salary = None
                max_salary = None


        vacancy_employer = vacancy.find('a',{'class' : 'bloko-link bloko-link_secondary'}).getText()
        vacancy_source = 'HeadHunter'

        vacancy_data['source'] = vacancy_source
        vacancy_data['name'] = vacancy_name
        vacancy_data['link'] = vacancy_link
        vacancy_data['employer'] = vacancy_employer
        vacancy_data['min_salary'] = min_salary
        vacancy_data['max_salary'] = max_salary
        jobs.append(vacancy_data)

    page += 1
    if vacancy_button == None:
        break

super_page = 1
while True:
    params = {'geo[t][0]' : 4 ,'page': super_page}
    html = requests.get(sl, params=params, headers=headers)
    soup = bs(html.text, 'html.parser')

    vacancy_pre_list = soup.find('div', {'class': '_3zucV _1fMKr undefined _3tcTB _3SGgo'})
    vacancy_block = vacancy_pre_list.parent
    vacancy_list = vacancy_block.find_all('div', {'class' : 'iJCa5 f-test-vacancy-item _1fma_ undefined _2nteL'}, recursive=True)
    vacancy_button = soup.find('a', {'class': 'icMQ_ _1_Cht _3ze9n f-test-button-dalshe f-test-link-Dalshe'})
    for vacancy in vacancy_list:
        vacancy_data = {}
        vacancy_name_1 = vacancy.find('span', {'class' : '_1rS-s'}).getText()
        vacancy_name = vacancy.find('span').getText()
        vacancy_link = super_link + vacancy.find('a')['href']
        vacancy_employer = vacancy.find('span', {'class': '_3mfro _3Fsn4 f-test-text-vacancy-item-company-name _9fXTd _2JVkc _2VHxz _15msI'}).getText()
        vacancy_source = 'SuperJob'
        vacancy_salary = vacancy.find('span', {'class' : '_3mfro _2Wp8I PlM3e _2JVkc _2VHxz'}).getText()
        if vacancy_salary:
            try:
                if 'от' in vacancy_salary:
                    salary_1 = re.findall(r'\d{2}.\d{3}', vacancy.find('span', {'class' : '_3mfro _2Wp8I PlM3e _2JVkc _2VHxz'}).getText())[0]
                    min_salary = float(salary_1.replace(u'\xa0', u''))
                    max_salary = None
                elif 'до' in vacancy_salary:
                    salary_2 = re.findall(r'\d{2}.\d{3}', vacancy.find('span', {'class' : '_3mfro _2Wp8I PlM3e _2JVkc _2VHxz'}).getText())[0]
                    min_salary = None
                    max_salary = float(salary_2.replace(u'\xa0',u''))
                elif 'По договоренности' in vacancy_salary:
                    min_salary = None
                    max_salary = None
                else:
                    salary_1 = re.findall(r'\d{2}.\d{3}', vacancy.find('span', {'class': '_3mfro _2Wp8I PlM3e _2JVkc _2VHxz'}).getText())[0]
                    salary_2 = re.findall(r'\d{2}.\d{3}', vacancy.find('span', {'class': '_3mfro _2Wp8I PlM3e _2JVkc _2VHxz'}).getText())[1]
                    min_salary = float(salary_1.replace(u'\xa0', u''))
                    max_salary = float(salary_2.replace(u'\xa0',u''))

            except:
                min_salary = None
                max_salary = None

        vacancy_data['source'] = vacancy_source
        vacancy_data['name'] = vacancy_name
        vacancy_data['link'] = vacancy_link
        vacancy_data['employer'] = vacancy_employer
        vacancy_data['min_salary'] = min_salary
        vacancy_data['max_salary'] = max_salary
        jobs.append(vacancy_data)

    super_page +=1
    if vacancy_button == None:
        break
# print(len(jobs))

df = pd.DataFrame.from_dict(jobs)
df = df[['name', 'link', 'employer', 'min_salary', 'max_salary', 'source']]
df.to_csv('vacancys_farma.csv', index = False)