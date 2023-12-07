import requests
from bs4 import BeautifulSoup
import json

# Шаг 1: Отправка HTTP запроса
url_basket_shop = 'https://www.basketshop.ru/catalog/shoes/'
response = requests.get(url_basket_shop)

def basket_shop(inp, gender):
  # Проверка успешности запроса
  if response.status_code == 200:
      soup = BeautifulSoup(response.text, 'html.parser')

      check_basket_shop = requests.get(url_basket_shop+inp.lower()+f'/{gender}')
      
      if check_basket_shop.status_code == 200:
        return url_basket_shop+inp.lower()+f'/{gender}'
      else:
        return False
  else:
      print(f"Ошибка при запросе: {response.status_code}")
      
links = []    
gender = input('Мужчина/женщина?:')

if gender == 'Мужчина':
  gender ='men'
elif gender == 'Женщина':
  gender = 'women'
  
inp = input('Введите нзвание бренда:')
check = basket_shop(inp, gender)

if check:
  links.append(check)
  print(f'ok\nLink:{links}')
elif check == False:
  print('error')
  
# test = input('Введите нзвание бренда:') 
# check_test = requests.get(f'https://www.google.com/search?q=basketshop+{test}')

# if check_test.status_code == 200:
#   print(f'https://www.google.com/search?q=basketshop+{test}')
# else:
#   print('error')

import requests
from bs4 import BeautifulSoup
from time import sleep

list_card_url = []

for count in range(1, 2):
    sleep(3)
    url = "https://www.basketshop.ru/catalog/shoes/"

    response = requests.get(url)

    soup = BeautifulSoup(response.text, "lxml")

    data = soup.find_all("div", class_="product-card")

    for i in data:
        card_url = "https://www.basketshop.ru" + i.find("a").get("href")
        list_card_url.append(card_url)


for card_url in list_card_url:
    response = requests.get(card_url)

    soup = BeautifulSoup(response.text, "lxml")

    all_cards = soup.find("div", class_="product__col product__col--2")

    main_head = all_cards.find("div", class_="product__head")

    name = main_head.find("h1", class_="product__title").text

    price = all_cards.find("div", class_="product__price-value").text
    print(name + "\n")
    print(price + "\n")
