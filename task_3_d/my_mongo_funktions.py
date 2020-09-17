from pymongo import MongoClient
from pprint import pprint

# Запись
def mongo_collection_writer(database, collection, vacancy_list):
    client = MongoClient('127.0.0.1', 27017)
    db = client[database]
    profession = db[collection]
    profession.insert_many(vacancy_list)
    return

# Вывод(проверка)
def show_mongo_collection(database, collection):
    client = MongoClient('127.0.0.1', 27017)
    db = client[database]
    for i in db[collection].find({}):
        pprint(i)

# Поиск по зп
def salary_search(database, collection, salary):
    client = MongoClient('127.0.0.1', 27017)
    db = client[database]
    vacancys = db[collection].find({'$or' : [{"min_salary" : {'$gt' : salary}}, \
                                             {"max_salary" : {'$gt' : salary}}]}, {'_id' : 0})
    for vacancy in vacancys:
        pprint(vacancy)

# Добавление новых вакансий
def append_new_vacancy(database, collection, vacancy_list):
    client = MongoClient('127.0.0.1', 27017)
    db = client[database]
    i = 0
    for vacancy in vacancy_list:
        if len([x for x in db[collection].find({'link' : vacancy['link']})]) == 0:
            db[collection].insert_one(vacancy)
            pprint(vacancy)
            i += 1
    print(f'{i} вакансий добавлено')

