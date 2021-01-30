import requests
from bs4 import BeautifulSoup
import csv
from datetime import datetime
import time

# https://coinmarketcap.com/all/views/all/   our target page

def get_html(url):
    r = requests.get(url)
    return r.text


def get_all_links(html):
    soup = BeautifulSoup(html, 'lxml')
    find_td = soup.find('tbody').find_all('div', class_='cmc-table__column-name')
    links = []

    for i in find_td:
        a = i.find('a').get('href')
        link = 'https://coinmarketcap.com' + a
        links.append(link)

    return links



def get_page_data(html):
    soup = BeautifulSoup(html, 'lxml')
    try:
        name = soup.find('h1', class_="priceHeading___2GB9O").text.strip()
    except:
        name = '___'

    try:
        price = soup.find('div', class_="priceValue___11gHJ").text.strip()
    except:
        price = '___'

    data = {'Name': name,
            'Price': price,}
    return data


def write_csv(data):
    with open('coinmarket.csv', 'a') as file:
        writer = csv.writer(file)
        writer.writerow( (data['Name'],
                          data['Price']) )
        print(data['Name'],'parsed')


def main():
    start = datetime.now()

    url = 'https://coinmarketcap.com/all/views/all/'

    all_links = get_all_links(get_html(url))

    for url in all_links:
        html = get_html(url)
        data = get_page_data(html)
        write_csv(data)
        time.sleep(1)


    end = datetime.now()

    total = end - start
    print(str(total))


if __name__ == '__main__':
    main()
