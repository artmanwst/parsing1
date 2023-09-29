import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import csv


count = 0
cap = 1
sleep = 100


def connect(url):
    options = Options()
    ua = UserAgent()
    options.add_argument(f"user-agent={ua.random}")
    options.add_argument("--headless")

    time.sleep(5)
    browser = webdriver.Chrome(options=options)
    browser.get(url)
    src = browser.page_source
    return src, browser


with open('top1000.csv', 'a', newline='', encoding='utf-8') as csv_file:
    csv_writer = csv.writer(csv_file)

    for i in range(2, 21):
        movie_blocks = []
        url = f'https://www.kinopoisk.ru/lists/movies/top_1000/?page={i}'
        src, browser = connect(url)
        soup = BeautifulSoup(src, 'lxml')
        movie_blocks = soup.find_all("div", class_="styles_content__nT2IG")
        print(f"Page {i} - URL: {url}")
        while len(movie_blocks) == 0:
            print(f'капча{cap}')
            cap += 1
            sleep += 20
            time.sleep(sleep)
            src, browser = connect(url)
            soup = BeautifulSoup(src, 'lxml')
        for movie_block in movie_blocks:
            movie_title = movie_block.find("span",
                                           class_="styles_mainTitle__IFQyZ")
            if movie_title:
                movie_title = movie_title.get_text(strip=True)
            else:
                movie_title = "Название фильма не найдено"

            year_span = movie_block.find("span", class_="desktop-list-main-info_secondaryText__M_aus")
            if year_span:
                year = year_span.get_text(strip=True)
                year = year.split()[0]
                if year[0] == ',':
                    year = year[1:]
                year = year[:-1]
            else:
                year = "Год создания не найден"

            rating_div = movie_block.find("div", class_="styles_kinopoisk__JZttS")
            if rating_div:
                rating_span = rating_div.find(['span', 'div'], class_=['styles_kinopoiskValuePositive__vOb2E', 'styles_kinopoiskValueNeutral__sW9QT', 'styles_empty__mT5M6'])
                if rating_span:
                    rating = rating_span.get_text(strip=True)
                else:
                    rating = "Оценка не найдена"
            else:
                rating = "Оценка не найдена"

            country_div = movie_block.find("div", class_="desktop-list-main-info_additionalInfo__Hqzof")
            if country_div:
                country_span = country_div.find("span", class_="desktop-list-main-info_truncatedText__IMQRP")
                if country_span:
                    country = country_span.get_text(strip=True)
                    country = country.split()[0]
                else:
                    country = "Страна не найдена"
            else:
                country = "Страна не найдена"
            director_divs = movie_block.find_all("div", class_="desktop-list-main-info_additionalInfo__Hqzof")
            director = "Режиссер не найден"
            for director_div in director_divs:
                if "Режиссёр:" in director_div.text:
                    director = director_div.text.replace("Режиссёр:", "").strip()
                    director = director.split()[3:]
                    director = ' '.join(director)
                    break
            watch_button = movie_block.find("div", class_="styles_onlineButton__ER9Vt styles_inlineItem___co22")
            if watch_button:
                watch_button_text = True
            else:
                watch_button_text=False
            print("Название фильма:", movie_title)
            print("Год создания:", year)
            print("Оценка:", rating)
            print("Страна:", country)
            print("Режиссер:", director)
            print('Возможность просмотра:', watch_button_text)
            print("-" * 50)
            csv_writer.writerow([movie_title, year, rating, country, director, watch_button_text])
        browser.quit()
