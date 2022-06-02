# Написать программу, которая собирает товары «В тренде» с сайта техники mvideo и складывает данные в БД.
# Сайт можно выбрать и свой. Главный критерий выбора: динамически загружаемые товары.

from pprint import pprint
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.keys import Keys
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError as dke

s = Service('./chromedriver.exe')
options = Options()
options.add_argument('start-maximized')
driver = webdriver.Chrome(service=s, options=options)
driver.implicitly_wait(10)
driver.get('https://www.mvideo.ru/')

client = MongoClient('127.0.0.1', 27017)
db = client['mvideo182']
collection = db.mvideo182_mongo

while True:
    try:
        button = driver.find_element(By.XPATH, "//span[contains(text(), 'В тренде')]")
        button.click()
        break
    except:
        driver.find_element(By.CLASS_NAME, 'popmechanic-desktop').send_keys(Keys.PAGE_DOWN)

# Хоть и не требовалось перелистывать, но я всё равно потренировался:
while True:
    try:
        button = driver.find_element(By.XPATH, "//mvid-carousel[@class='carusel ng-star-inserted']/div[@class='button-size--medium buttons']/button[@class='btn forward mv-icon-button--primary mv-icon-button--shadow mv-icon-button--medium mv-button mv-icon-button']")
        button.click()
    except:
        break

goods = driver.find_element(By.XPATH, "//mvid-shelf-group[@class='page-carousel-padding ng-star-inserted']")

# goods = trends.find_elements(By.XPATH, "./ancestor::mvid-shelf-group")

names = goods.find_elements(By.XPATH, "//div[@class='title']")
links = goods.find_elements(By.XPATH, "//div[@class='title']/a[@href]")
prices = goods.find_elements(By.XPATH, "//div[@class='product-mini-card__price ng-star-inserted']//span[@class='price__main-value']")

good = {}

for name, link, price in zip(names, links, prices):

    good['name'] = name.text
    good['link'] = link.get_attribute("href")
    good['price'] = price.text

    try:
        collection.update_one({'link': good['link']}, {'$set': good}, upsert=True)
    except dke:
        print(f'Пытаемся добавить такой же элемент!..')

    # collection.insert_one(good)

result = list(collection.find({}))
pprint(result)