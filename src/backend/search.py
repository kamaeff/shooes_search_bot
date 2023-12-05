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