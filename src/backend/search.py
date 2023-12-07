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
