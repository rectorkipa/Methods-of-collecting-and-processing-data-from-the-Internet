# 1. Развернуть у себя на компьютере/виртуальной машине/хостинге MongoDB и реализовать функцию,
# которая будет добавлять только новые вакансии в вашу базу.

# 2. Написать функцию, которая производит поиск и выводит на экран вакансии с заработной платой больше
# введённой суммы (необходимо анализировать оба поля зарплаты).

from bs4 import BeautifulSoup as bs
import requests
from pprint import pprint
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
import hashlib


main_url = 'https://hh.ru/'
page = 0
params = {'text': 'python',
          'items_on_page': 20,
          'page': page}
headers = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) '
                         'AppleWebKit/537.36 (KHTML, like Gecko) '
                         'Chrome/101.0.4951.64 Safari/537.36'}

response = requests.get(main_url+'search/vacancy', params=params, headers=headers)

soup = bs(response.text, 'html.parser')

try:
    last_page = int(soup.find_all('a',{'data-qa':'pager-page'})[-1].text)
except:
    last_page = 1

for i in range(last_page):

    vacancies = soup.find_all('div', {'class': 'vacancy-serp-item-body__main-info'})

    all_vacancies = []

    for vacancy in vacancies:
        vacancy_info = {}

        vacancy_name = vacancy.find('a').getText()
        vacancy_info['vacancy_name'] = vacancy_name

        vacancy_link = vacancy.find('a', {'class': 'bloko-link'})['href']
        vacancy_info['vacancy_link'] = vacancy_link

        vacancy_salary = vacancy.find('span', {'data-qa': "vacancy-serp__vacancy-compensation"})
        if vacancy_salary is None:
            min_salary = None
            max_salary = None
            currency = None
        else:
            vacancy_salary = vacancy_salary.getText()
            if vacancy_salary.startswith('до'):
                max_salary = int("".join([s for s in vacancy_salary.split() if s.isdigit()]))
                min_salary = None
                currency = vacancy_salary.split()[-1]

            elif vacancy_salary.startswith('от'):
                max_salary = None
                min_salary = int("".join([s for s in vacancy_salary.split() if s.isdigit()]))
                currency = vacancy_salary.split()[-1]

            else:
                max_salary = int("".join([s for s in vacancy_salary.split('–')[1] if s.isdigit()]))
                min_salary = int("".join([s for s in vacancy_salary.split('–')[0] if s.isdigit()]))
                currency = vacancy_salary.split()[-1]

        vacancy_info['max_salary'] = max_salary
        vacancy_info['min_salary'] = min_salary
        vacancy_info['currency'] = currency

        vacancy_info['vacancy_site'] = 'hh.ru'

        all_vacancies.append(vacancy_info)

    # pprint(all_vacancies)

    params['page'] += + 1


client = MongoClient('127.0.0.1', 27017)

db = client['vacancies182']

collection = db.vacancies_mongo


# 1.

# Хеширрование по ссылке, так как она уникальна:
link_pre_encode = vacancy_link.encode()
link_encode = hashlib.sha256(link_pre_encode)
link_hex = link_encode.hexdigest()

# Добавление нового поля ID:
vacancy_info['_id'] = link_hex

# Добавление в коллекцию:
try:
    collection.insert_one(vacancy_info)
except DuplicateKeyError:
    print(f'Документ с идентификатором {link_hex} уже существует!')

# result = list(collection.find({}))
# pprint(result)


# 2.

salary_min = int(input('Введите минимальную зарплату: '))

# Ищем данные, подходящие под условие, по обоим полям:
def hot_salary():
    hot_vacancies = collection.find({'$or': [{'min_salary': {'$gt': salary_min}}, {'max_salary': {'$gt': salary_min}}]})
    for hot_vacancy in hot_vacancies:
        pprint(hot_vacancy)

hot_salary()