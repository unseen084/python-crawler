import time

import requests
import pandas as pd
from bs4 import BeautifulSoup


def crawler(url):
    prod_list = []
    page = 1
    total_products = 0
    while True:
        r = requests.get(url + str(page))
        page += 1
        soup = BeautifulSoup(r.content, 'html.parser')
        content = soup.find_all('div', class_='p-item-inner')
        total_products += len(content)
        if len(content) == 0:
            break
        for item in content:
            name = item.findNext('h4', class_='p-item-name').text
            product_link = item.findNext('a')['href']
            price = item.findNext('div', class_='p-item-price').text
            image_link = item.find('div', class_='p-item-img').img['src']
            image_name = item.find('div', class_='p-item-img').img['alt']

            product_info = {
                'name': name,
                'product_link': product_link,
                'price': price,
                'image_link': image_link,
                'image_name': image_name
            }
            prod_list.append(product_info)
        print(total_products)
        time.sleep(2)
    return prod_list


product_list = crawler('https://www.startech.com.bd/monitor?page=')
df = pd.DataFrame(product_list)
df.to_csv('gaming_monitor_list.csv')
