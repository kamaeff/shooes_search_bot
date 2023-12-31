import requests
import os
from bs4 import BeautifulSoup
from urllib.parse import urljoin

url = f"https://www.basketshop.ru/catalog/shoes/"


async def basket_shop(brand, gender):
    print(brand, gender)
    for count in range(1, 2):

        new_url = f"{brand}/{gender}/lifestyle;oncourt/"
        print(f"url: {url}\nnew_url: {url + new_url}")
        list_card_url = []

        response = requests.get(url + new_url)
        if (response.status_code == 200):
            # print(f"response: {response.status_code}")
            soup = BeautifulSoup(response.text, "lxml")

            data = soup.find_all("div", class_="product-card")

            for i in data:
                card_url = "https://www.basketshop.ru" + \
                    i.find("a").get("href")
                list_card_url.append(card_url)

            return list_card_url

        else:
            return False


async def download_image(image_url, folder_path, image_name):
    file_path = os.path.join(folder_path, image_name)
    try:
      if os.path.exists(file_path):
        print(f"Фото {image_name} уже существует в папке {folder_path}.")
      else:
        response = requests.get(image_url)
        if response.status_code == 200:
            print(f"response: {response.status_code}")
            image_path = os.path.join(folder_path, image_name)
            with open(image_path, 'wb') as f:
                f.write(response.content)
            print(f"Downloaded: {image_path}")
        else:
            print(f"Failed to download image: {image_url}")

        return image_path
    except Exception as e:
        print(f"Exception: {e}")


async def parsing(userStorage, chat_id):

    print(userStorage[chat_id])
    check = await basket_shop(userStorage[chat_id]['_list'], userStorage[chat_id]['selected_gender'])

    if check == False:
        return False, userStorage[chat_id]['_list']
    else:
        item_info = []
        image_src = []
        for card_url in check:
            response = requests.get(card_url)

            soup = BeautifulSoup(response.text, "lxml")

            # Получение тайтла и цены пары
            all_cards = soup.find("div", class_="product__col product__col--2")
            main_head = all_cards.find("div", class_="product__head")
            name = main_head.find("h1", class_="product__title").text
            price = all_cards.find("div", class_="product__price-value").text

            price = price.replace('\t', '')
            price = price.replace('\n', '')

            item_info.append([[name], [price]])

            # Поиск картики
            slide_class = soup.find(
                "div", class_="product__gallery-slider-slide-cell")
            image_src.append(slide_class.find("img")["src"])

        print("Image Source:", image_src, len(image_src))
        for idx in range(len(image_src)):
            image_url = urljoin(card_url, image_src[idx])
            await download_image(image_url, "./src/backend/gen_imgs/",
                           f"{userStorage[chat_id]['_list']}_{idx}_{userStorage[chat_id]['selected_gender']}_basketshop.jpg")

        return item_info, url+f"{userStorage[chat_id]['_list']}/{userStorage[chat_id]['selected_gender']}/lifestyle;oncourt/"
