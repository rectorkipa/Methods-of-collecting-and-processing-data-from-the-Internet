# 1. Написать приложение, которое собирает основные новости с сайта на выбор news.mail.ru, lenta.ru, yandex-новости.
# Для парсинга использовать XPath. Структура данных должна содержать:
# - название источника;
# - наименование новости;
# - ссылку на новость;
# - дата публикации.
# 2. Сложить собранные новости в БД

from lxml import html
import requests
from pprint import pprint
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke

url = 'https://lenta.ru/'
headers = {'user-agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.64 Safari/537.36'}

response = requests.get(url, headers=headers)

dom = html.fromstring(response.text)

items = dom.xpath("//a[contains(@class, 'card-mini')]")

list_items = []

for item in items:

    item_info = {}

    source = 'lenta.ru'
    name = item.xpath(".//span[contains(@class, 'card-mini__title')]/text()")[0]
    link = url + item.xpath("./@href")[0]
    date = item.xpath(".//time[@class='card-mini__date']/text()")

    item_info['source'] = source
    item_info['name'] = name
    item_info['link'] = link
    item_info['date'] = date

    list_items.append(item_info)

# pprint(list_items)


client = MongoClient('127.0.0.1', 27017)

db = client['news182']

collection = db.news182_mongo

try:
    collection.insert_many(list_items)
except dke:
    print(f'Пытаемся добавить такой же элемент!..')

result = list(collection.find({}))
pprint(result)