# Необходимо собрать информацию о вакансиях на вводимую должность
# (используем input или через аргументы получаем должность) с сайтов HH(обязательно) и/или Superjob(по желанию).
# Приложение должно анализировать несколько страниц сайта (также вводим через input или аргументы).
# Получившийся список должен содержать в себе минимум:
# 1. Наименование вакансии.
# 2. Предлагаемую зарплату (разносим в три поля: минимальная и максимальная и валюта. цифры преобразуем к цифрам).
# 3. Ссылку на саму вакансию.
# 4. Сайт, откуда собрана вакансия.
# По желанию можно добавить ещё параметры вакансии (например, работодателя и расположение).
# Структура должна быть одинаковая для вакансий с обоих сайтов.
# Общий результат можно вывести с помощью dataFrame через pandas.
# Сохраните в json либо csv.

from bs4 import BeautifulSoup as bs
import requests
import json
# from pprint import pprint
# import pandas as pd

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

        vacancy_site = vacancy.parent.parent.parent.parent.parent.parent.parent.parent.parent.parent.parent.parent.parent.parent.parent.parent.find('title').getText()
        vacancy_info['vacancy_site'] = vacancy_site

        all_vacancies.append(vacancy_info)

    # pprint(all_vacancies)

    params['page'] += + 1

# df = pd.DataFrame(all_vacancies)
# df

with open('vacancies.json', 'w') as f:
    json.dump(all_vacancies, f)