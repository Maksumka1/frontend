import psycopg2
from prometheus_client import start_http_server, Counter, Gauge
import requests 
import json
import logging
import os
import time
from bs4 import BeautifulSoup

os.makedirs('logs', exist_ok=True)

logging.basicConfig(
    filename='logs/crypto.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

parsed_pages = Counter('parser_pages_total', 'Скільки сторінок спарсено')
errors_total = Counter('parser_errors_total', 'Кількість помилок')
badPc_total = Counter('parser_bad_total', 'Кількість поганих компів')
parsing_time = Gauge('parser_last_duration_seconds', 'Час останнього парсингу')
parser_restart_counter = Counter('parser_restart_total', 'Кількість запусків парсера')
process_time_total = Counter('process_time_total', 'Загальний час роботи програми')

parser_restart_counter.inc()
def linkResponce(url):
    responce = requests.get(url)
    soup = BeautifulSoup(responce.text, 'lxml')
    return soup

best_pcs = {}
with open('./links.json', 'r') as file:
    best_pcs = json.load(file)

start_time = time.time()

while True:
    try:
        conn = psycopg2.connect(
            host='db',
            dbname='mydb',
            user='postgres',
            password='password123',
            port=5432
        )
        print("Connected to Postgres!")
        break
    except psycopg2.OperationalError:
        print("Postgres not ready, retrying in 2s...")
        time.sleep(2)

cur = conn.cursor()

start_http_server(5001)


def search():
    print('Початок')
    # computerLinks = ['https://www.olx.ua/uk/elektronika/kompyutery-i-komplektuyuschie/nastolnye-kompyutery/q-%D1%96%D0%B3%D1%80%D0%BE%D0%B2%D0%B8%D0%B9-%D0%BF%D0%BA/?currency=UAH&search%5Bfilter_float_price:from%5D=2000&search%5Bfilter_float_price:to%5D=11000', 'https://www.olx.ua/uk/elektronika/kompyutery-i-komplektuyuschie/nastolnye-kompyutery/q-%D1%96%D0%B3%D1%80%D0%BE%D0%B2%D0%B8%D0%B9-%D0%BF%D0%BA/?currency=UAH&page=2&search%5Bfilter_float_price%3Afrom%5D=2000&search%5Bfilter_float_price%3Ato%5D=11000', 'https://www.olx.ua/uk/elektronika/kompyutery-i-komplektuyuschie/nastolnye-kompyutery/q-%D1%96%D0%B3%D1%80%D0%BE%D0%B2%D0%B8%D0%B9-%D0%BF%D0%BA/?currency=UAH&page=3&search%5Bfilter_float_price%3Afrom%5D=2000&search%5Bfilter_float_price%3Ato%5D=11000']
    upperPrice = 14000
    computerLinks = [
        f'https://www.olx.ua/uk/elektronika/kompyutery-i-komplektuyuschie/nastolnye-kompyutery/q-%D1%96%D0%B3%D1%80%D0%BE%D0%B2%D0%B8%D0%B9-%D0%BF%D0%BA/?currency=UAH&page=1&search%5Bfilter_float_price%3Afrom%5D=2900&search%5Bfilter_float_price%3Ato%5D={upperPrice}',
        f'https://www.olx.ua/uk/elektronika/kompyutery-i-komplektuyuschie/nastolnye-kompyutery/q-%D1%96%D0%B3%D1%80%D0%BE%D0%B2%D0%B8%D0%B9-%D0%BF%D0%BA/?currency=UAH&page=2&search%5Bfilter_float_price%3Afrom%5D=2900&search%5Bfilter_float_price%3Ato%5D={upperPrice}',
        f'https://www.olx.ua/uk/elektronika/kompyutery-i-komplektuyuschie/nastolnye-kompyutery/q-%D1%96%D0%B3%D1%80%D0%BE%D0%B2%D0%B8%D0%B9-%D0%BF%D0%BA/?currency=UAH&page=3&search%5Bfilter_float_price%3Afrom%5D=2900&search%5Bfilter_float_price%3Ato%5D={upperPrice}', 

        f'https://www.olx.ua/uk/elektronika/kompyutery-i-komplektuyuschie/nastolnye-kompyutery/q-%D0%BF%D0%BA/?currency=UAH&page=1&search%5Bfilter_float_price%3Afrom%5D=2900&search%5Bfilter_float_price%3Ato%5D={upperPrice}', 
        f'https://www.olx.ua/uk/elektronika/kompyutery-i-komplektuyuschie/nastolnye-kompyutery/q-%D0%BF%D0%BA/?currency=UAH&page=2&search%5Bfilter_float_price%3Afrom%5D=2900&search%5Bfilter_float_price%3Ato%5D={upperPrice}', 
        f'https://www.olx.ua/uk/elektronika/kompyutery-i-komplektuyuschie/nastolnye-kompyutery/q-%D0%BF%D0%BA/?currency=UAH&page=3&search%5Bfilter_float_price%3Afrom%5D=2900&search%5Bfilter_float_price%3Ato%5D={upperPrice}', 

        f'https://www.olx.ua/uk/elektronika/kompyutery-i-komplektuyuschie/nastolnye-kompyutery/q-%D0%BA%D0%BE%D0%BC%D0%BF%D1%8E%D1%82%D0%B5%D1%80/?currency=UAH&page=1&search%5Bfilter_float_price%3Afrom%5D=2900&search%5Bfilter_float_price%3Ato%5D={upperPrice}', 
        f'https://www.olx.ua/uk/elektronika/kompyutery-i-komplektuyuschie/nastolnye-kompyutery/q-%D0%BA%D0%BE%D0%BC%D0%BF%D1%8E%D1%82%D0%B5%D1%80/?currency=UAH&page=2&search%5Bfilter_float_price%3Afrom%5D=2900&search%5Bfilter_float_price%3Ato%5D={upperPrice}', 
        f'https://www.olx.ua/uk/elektronika/kompyutery-i-komplektuyuschie/nastolnye-kompyutery/q-%D0%BA%D0%BE%D0%BC%D0%BF%D1%8E%D1%82%D0%B5%D1%80/?currency=UAH&page=3&search%5Bfilter_float_price%3Afrom%5D=2900&search%5Bfilter_float_price%3Ato%5D={upperPrice}', 

        f'https://www.olx.ua/uk/elektronika/kompyutery-i-komplektuyuschie/nastolnye-kompyutery/q-%D1%96%D0%B3%D1%80%D0%BE%D0%B2%D0%B8%D0%B9-%D0%BA%D0%BE%D0%BC%D0%BF%D1%8E%D1%82%D0%B5%D1%80/?currency=UAH&page=1&search%5Bfilter_float_price%3Afrom%5D=2900&search%5Bfilter_float_price%3Ato%5D={upperPrice}', 
        f'https://www.olx.ua/uk/elektronika/kompyutery-i-komplektuyuschie/nastolnye-kompyutery/q-%D1%96%D0%B3%D1%80%D0%BE%D0%B2%D0%B8%D0%B9-%D0%BA%D0%BE%D0%BC%D0%BF%D1%8E%D1%82%D0%B5%D1%80/?currency=UAH&page=2&search%5Bfilter_float_price%3Afrom%5D=2900&search%5Bfilter_float_price%3Ato%5D={upperPrice}',
        f'https://www.olx.ua/uk/elektronika/kompyutery-i-komplektuyuschie/nastolnye-kompyutery/q-%D1%96%D0%B3%D1%80%D0%BE%D0%B2%D0%B8%D0%B9-%D0%BA%D0%BE%D0%BC%D0%BF%D1%8E%D1%82%D0%B5%D1%80/?currency=UAH&page=3&search%5Bfilter_float_price%3Afrom%5D=2900&search%5Bfilter_float_price%3Ato%5D={upperPrice}'
    ]
    for link in computerLinks:
        brain(link)

def bad_check(advert_url, description):
    bad_conditions = ['HP', 'Acer', 'Dell','i5-33', 'i7-860', 'i7 860','i7-26', 'i7 26', 'I7 2', 'i7 3', 'I7-3', 'i7-3', 'i7 4', 'i7-4', 'і7 4', 'I7-4', 'I7 4','i5 33', 'i5-23', 'i5 23', 'i5 2', 'i5-44', 'i5 44', 'I5- 4', 'I5 4', 'I5 - 4', 'і5-4', 'FX', 'fx', 'Fx','i5-35', 'i5 35', 'Xeon', 'xeon', 'i5-34', 'i5-3', 'i5 3', 'і5 3', 'I5-3', 'і5-3', 'I5 3', 'I5-2', 'I5 2', 'і5 2', 'і5-2', 'i5 2', 'i5-2', 'i5 4', 'i5-4', 'i3 4', 'i3-3', 'i3-2', 'Athlon', 'ATHLON', 'athlon', 'atlo', 'A8', 'A10', 'A6', 'Phenom', 'phenom', 'XEON', 'xeon', 'Xeon', '2620', 'fujitsu', 'Fujit', 'Lenovo']
    if any(bad_word in description for bad_word in bad_conditions) or len(description) < 86 or len(description.replace(' ', '')) > 600:
        logging.info(f'Це поганий компютер: {advert_url}')
        badPc_total.inc()
        return 0
    return 1



def brain(link):
    soup = linkResponce(link)
    advertisament = soup.find_all('div', class_='css-1r93q13')
    for i in advertisament:
        try:
            start = time.time()
            advert_url = "https://www.olx.ua" + i.find('a').get('href')
            soup = linkResponce(advert_url)

            description = soup.find('div', class_='css-19duwlz').text
            price = soup.find('h3', class_='css-yauxmy').text
            photo = soup.find('img', class_='css-1bmvjcs').get('src')
            title = soup.find('h4', class_='css-1au435n').text.replace("'", "")

            process_time_total.inc(start_time)
            parsed_pages.inc()

            if advert_url not in best_pcs:
                if bad_check(advert_url, description) == 0:
                    continue
                else:
                    best_pcs[advert_url] = photo
                    cur.execute("""
                    INSERT INTO person (name, image_url, description, price, title) 
                    VALUES (%s, %s, %s, %s, %s);
                    """, (advert_url, photo, description, price, title))
                    logging.info(f'Пк пройшов перевірку --> {advert_url}')
            
            parsing_time.set(time.time() - start)

        except AttributeError as fail: 
            errors_total.inc()
            logging.error(f'Помилка при запиті до OLX: {fail}')
            continue

search()
conn.commit()

cur.close()
conn.close()
print(best_pcs)


end_time = time.time()
elapsed_time = end_time - start_time
print(f"Час виконання: {elapsed_time:.2f} секунд")

with open('links.json', 'w') as file:
    json.dump(best_pcs, file, indent=4)
