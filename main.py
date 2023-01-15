import requests
import re
from bs4 import BeautifulSoup
from fake_headers import Headers
import json

HOST = 'https://spb.hh.ru/search/vacancy?text=python&area=1&area=2'


def get_headers():
    return Headers(browser='chrome', os='win').generate()


pars = requests.get(HOST, headers=get_headers()).text
soup = BeautifulSoup(pars, features='lxml')

vacancies = soup.findAll('div', class_='serp-item')
data = []

for vacancy in vacancies:
    f_work = vacancy.find('div', class_='g-user-content').text
    pattern2 = re.compile("Django?|Flask?|django?|flask?")
    f_work2 = pattern2.findall(f_work)
    print(f_work2)

    if 'Flask' and 'Django' in f_work2:
        email = vacancy.find('a', class_='serp-item__title').get('href')
        salary_raw = vacancy.find('span', class_='bloko-header-section-3')
        if salary_raw is not None:
            salary = vacancy.find('span', class_='bloko-header-section-3').text
        else:
            salary = 'з/п не указана'

        company = vacancy.find('a', class_='bloko-link_kind-tertiary').text
        city_raw = vacancy.find('div', class_='vacancy-serp-item-company').text
        pattern = re.compile("Москва?|Санкт-Петербург?")
        city = pattern.findall(city_raw)
        data.append({
            'email': email,
            'salary': salary.replace(u"\u202F", " "),
            'company': company,
            'city': city[0]
        })

with open("result.json", "w") as f:
    json.dump(data, f, ensure_ascii=False, indent=2)
