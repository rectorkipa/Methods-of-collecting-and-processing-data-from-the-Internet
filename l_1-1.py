# 1. Посмотреть документацию к API GitHub,
# разобраться как вывести список репозиториев для конкретного пользователя,
# сохранить JSON-вывод в файле *.json.

import requests
import json

url = 'https://api.github.com/users/rectorkipa/repos'

response = requests.get(url)

j_data = response.json()

repos = []
for i in j_data:
    repos.append(i['name'])

print('Список репозиториев конкретного пользователя "rectorkipa": ', repos)

with open('repos.json', 'w') as f:
    json.dump(j_data, f)