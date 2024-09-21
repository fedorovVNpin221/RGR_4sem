import os
import requests
from bs4 import BeautifulSoup

def parse():
    headers = {
        'User-Agent': 'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14'
    }

    feedlist = {
        'rbc': 'https://www.rbc.ru/short_news/',
        'ria_all': 'https://ria.ru/lenta/',
        'ria_world': 'https://ria.ru/world/',
        'lenta_all': 'https://lenta.ru/parts/news/2/',
        'lenta_russia': 'https://lenta.ru/rubrics/russia/',
        'sport': 'https://www.sports.ru/news/',
        'iz_all': 'https://iz.ru/news',
        'panorama_s': 'https://panorama.pub/science',
        'panorama_e': 'https://panorama.pub/economics',
        'ria_med': 'https://ria.ru/tag_medicina/'
    }

    for key, url in feedlist.items():
        headlines_list = []
        print(url)
        page = requests.get(url, headers=headers)
        print(page.status_code)
        soup = BeautifulSoup(page.text, "lxml")

        if key == 'rbc':
            headlines = soup.find_all("span", class_="normal-wrap")
        elif key.startswith('ria'):
            headlines = soup.find_all("a", class_="list-item__title color-font-hover-only")
        elif key.startswith('lenta'):
            headlines = soup.find_all("h3")
        elif key == 'sport':
            headlines = soup.find_all('a', class_='short-text')
        elif key.startswith('panorama'):
            headlines = soup.find_all('div', class_='pt-2 text-xl lg:text-lg xl:text-base text-center font-semibold')
        else:
            headlines = soup.find_all('div', class_='node__cart__item__inside__info__title small-title-style1')

        count = 0
        for headline in headlines:
            if count >= 30:
                break
            headline_text = headline.text.strip()
            if headline_text not in headlines_list:
                headlines_list.append(headline_text)
                print(headline_text)
                count += 1

        file_save_func(key, headlines_list)

def file_save_func(key, headlines_list):
    folder_name = "titles"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)

    filename = f"{folder_name}/{key}_headlines.txt"

    with open(filename, "w", encoding="utf-8") as file:
        for headline in headlines_list:
            file.write(headline + "\n")
        print(f"Файл {filename} успешно создан и заголовки сохранены.")

if __name__ == "__main__":
    parse()
