import requests
from bs4 import BeautifulSoup
import os


def stock_bar_parse():
    headers = {
        'User-Agent': 'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14'
    }
    url = 'https://finance.yahoo.com/calendar/'
    print(url)
    page = requests.get(url, headers=headers)
    print(page.status_code)
    soup = BeautifulSoup(page.content, "lxml")
    stock_link_list = []
    stock_title_list = []

    company_data = soup.find('div',
                             class_='Bgc($lv2BgColor) Bxz(bb) Ovx(a) Pos(r) Maw($newGridWidth) Miw($minGridWidth) Miw(a)!--tab768 Miw(a)!--tab1024 Mstart(a) Mend(a) Px(20px) Py(10px) D(n)--print')
    if company_data:
        company_list = company_data.find_all('li')
        for item in company_list:
            link = item.find('a')['href']
            title = item.find('a')['title']
            stock_link_list.append(link)
            stock_title_list.append(title)

    title_link_dict = dict(zip(stock_title_list, stock_link_list))  # Создание словаря из списков
    print(title_link_dict)
    action_data_dict = stock_action_parse(title_link_dict)
    save_data_to_file(action_data_dict)


def stock_action_parse(title_link_dict):
    headers = {
        'User-Agent': 'Opera/9.80 (Windows NT 6.0) Presto/2.12.388 Version/12.14'
    }

    action_data_dict = {}
    for title, link in title_link_dict.items():
        url = f"https://finance.yahoo.com{link}"
        page = requests.get(url, headers=headers)
        soup = BeautifulSoup(page.content, "lxml")
        container = soup.find('div', class_='container svelte-tx3nkj').find_all('li', class_='svelte-tx3nkj')

        date = soup.find('div', class_='container svelte-tx3nkj').find('li', class_='last-lg svelte-tx3nkj').find(
            'span', class_='value svelte-tx3nkj').text
        open_price = soup.find('div', class_='container svelte-tx3nkj').find('li', class_='last-md svelte-tx3nkj').find(
            'span', class_='value svelte-tx3nkj').text
        low_high_price = soup.find('div', class_='container svelte-tx3nkj').find('li', class_='last-md last-lg svelte-tx3nkj').find(
            'span', class_='value svelte-tx3nkj').text
        volume = soup.find('div', class_='container svelte-tx3nkj').find('fin-streamer', class_='svelte-tx3nkj').text

        close_price = []
        count = 0
        for element in container:
            z = element.find('span', class_='value svelte-tx3nkj').text
            count += 1
            if count == 5:
                close_price.append(z)
            else:
                continue

        volume = volume.replace("k", "0").replace(".", "")
        open_price = open_price.replace(",", ".")
        close_price = [price.replace(',', '.') for price in close_price]
        low_high_price_cleaned = low_high_price.replace('-', '')  # Удаление всех символов "-"
        low_high_price_list = [price.replace(',', '.') for price in low_high_price_cleaned.split() if price != '-']

        # Поменять местами значения в списке
        for i in range(0, len(low_high_price_list) - 1, 2):
            low_high_price_list[i], low_high_price_list[i + 1] = low_high_price_list[i + 1], low_high_price_list[i]

        action_data_dict[title] = f"{date} {open_price} {low_high_price_list} {close_price} {volume} {close_price}"

    print(action_data_dict)

    return action_data_dict


def save_data_to_file(action_data_dict):
    folder_name = "stock"
    if not os.path.exists(folder_name):
        os.makedirs(folder_name)
    for title, date in action_data_dict.items():
        filename = f"{folder_name}/{title}_data.txt"
        cleaned_date = date.replace("'", "").replace("[", "").replace("]", "").replace(" ", ", ").replace(",, ", ", ").replace(", , ", ", ")
        with open(filename, 'w') as file:
            file.write(cleaned_date)

stock_bar_parse()

