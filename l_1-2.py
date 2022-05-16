# 2. Изучить список открытых API (https://www.programmableweb.com/category/all/apis).
# Найти среди них любое, требующее авторизацию (любого типа).
# Выполнить запросы к нему, пройдя авторизацию. Ответ сервера записать в файл.
# Если нет желания заморачиваться с поиском, возьмите API вконтакте (https://vk.com/dev/first_guide).
# Сделайте запрос, чтобы получить список всех сообществ на которые вы подписаны.

import requests
import json

url = 'https://api.vk.com/method/groups.get?user_id=55369256&access_token=27b157e4334d45606e422e1807d2a538887a8f40156c75340193f225cafdb2746b18071c05d7900307b58&v=5.131'

response = requests.get(url)

j_data = response.json()

print('Список всех сообществ: ', j_data)

with open('vk_groups.json', 'w') as f:
    json.dump(j_data, f)