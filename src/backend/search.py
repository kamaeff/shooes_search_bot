import requests
from bs4 import BeautifulSoup
from time import sleep


def download(url):
    resp = requests.get(url, stream=True)
    # создаем файл в котором запишем байты изооброжения
    r = open("C:\\Users\\User\\Desktop\\img\\" + url.split("/")[-1], "wb")
    for value in resp.iter_content(1024 * 1024):
        r.write(value)
    r.close()


def get_url():
    for count in range(1, 2):
        url = "https://www.basketshop.ru/catalog/shoes/"

        response = requests.get(url)

        soup = BeautifulSoup(response.text, "lxml")

        data = soup.find_all("div", class_="product-card")

        for i in data:
            card_url = "https://www.basketshop.ru" + i.find("a").get("href")
            yield card_url


def array():
    for card_url in get_url():
        response = requests.get(card_url)
        sleep(2)
        soup = BeautifulSoup(response.text, "lxml")
        # переход в карточки обуви
        all_cards = soup.find("div", class_="product__col product__col--2")
        # карточка продукта
        main_head = all_cards.find("div", class_="product__head")
        # Нахождение названия кроссовок
        name = main_head.find("h1", class_="product__title").text
        # Нахождение цены
        price = all_cards.find("div", class_="product__price-value").text
        # Ссылки картинок
        img_part = soup.find("div", class_="product__gallery-slider-slide-cell js-zoom")
        url_img = img_part.find("img").get("src")
        download(url_img)
        yield name, price, url_img
