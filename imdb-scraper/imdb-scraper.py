
import argparse
import random
import re
import sys
import webbrowser
from pathlib import Path

import pandas as pd
import requests
from bs4 import BeautifulSoup
from PyQt6.QtCore import QObject, pyqtSlot
from PyQt6.QtGui import QGuiApplication, QIcon
from PyQt6.QtQml import QQmlApplicationEngine

TITLE_PATTERN = r"(\w+)\.\n[\s\t]+([\S\s]+)\n\((\w+)"

CHROME_PATH = "C:\\Program Files (x86)\\Google\\Chrome\\Application\\chrome.exe"
CHROME_PATH_X86 = "C:\\Program Files\\Google\\Chrome\\Application\\chrome.exe"
if Path(CHROME_PATH).exists():
    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(CHROME_PATH))
elif Path(CHROME_PATH_X86).exists():
    webbrowser.register('chrome', None, webbrowser.BackgroundBrowser(CHROME_PATH_X86))
else:
    print("Warning. No Google Chrome path found!")

class IMDbScraper(QObject):
    BASE_URL = "http://www.imdb.com"
    TOP250_URL = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"

    def __init__(self, *args, **kwargs):
        super(IMDbScraper, self).__init__(*args, **kwargs)

        self.soup = self._scrape_imdb()
        self.top_250 = self._extract_top_250()

    def _scrape_imdb(self):
        page = requests.get(self.TOP250_URL)
        soup = BeautifulSoup(page.content, "html.parser")
        return soup

    @staticmethod
    def _add_title_data(movie_element, movie_dict):
        title_element = movie_element.find("td", class_="titleColumn")
        title_text = title_element.text.strip()
        url_ref = title_element.find("a")["href"]

        result = re.match(TITLE_PATTERN, title_text)
        movie_dict["Rank"] = result.group(1)
        movie_dict["Title"] = result.group(2)
        movie_dict["Year"] = result.group(3)
        movie_dict["URL"] = url_ref
        return movie_dict

    @staticmethod
    def _add_rating_data(movie_element, movie_dict):
        rating_elements = movie_element.find_all("td", class_="ratingColumn")
        # Extract IMDB rating.
        imdb_rating_element = rating_elements[0]
        imdb_rating = imdb_rating_element.text.strip()
        movie_dict["Rating"] = imdb_rating

        # Extract user rating.
        # TODO(fredrikw): DOESN'T WORK!
        # rating = rating_elements[1].find("div", class_="rating").text
        # print(rating)
        return movie_dict

    def _extract_top_250(self):
        # Extract all movie elements.
        movie_elements = self.soup.find("tbody", class_="lister-list").find_all("tr")

        # Loop over all movies and extract data.
        imdb_top_250 = []
        for movie_element in movie_elements:
            movie_dict = {}
            movie_dict = self._add_title_data(movie_element, movie_dict)
            movie_dict = self._add_rating_data(movie_element, movie_dict)
            imdb_top_250.append(movie_dict)

        return imdb_top_250

    def get_top_250(self):
        return pd.DataFrame(self.top_250)

    def recommend(self):
        idx = random.randint(0, 249)
        return self.top_250[idx]

    @pyqtSlot()
    def open_recommended(self):
        movie = self.recommend()
        title_url = self.BASE_URL + movie["URL"]
        webbrowser.get("chrome").open(title_url)

def print_recommended_movie(imdb_scraper):
    movie = imdb_scraper.recommend()
    print("\nThe randomly chosen movie was:\n")
    print(f'# {movie["Rank"]}. {movie["Title"]} ({movie["Year"]}) Rating: {movie["Rating"]}\n')

def print_all_movies(imdb_scraper):
    imdb_df = imdb_scraper.get_top_250()
    print(imdb_df.to_string(index=False))

def parse_args():
    parser = argparse.ArgumentParser(description="IMDB movie selection.")
    parser.add_argument("--recommend", action="store_true", help="Select movie randomly.")
    parser.add_argument("--show", action="store_true", help="Show all movies.")
    parser.add_argument("--gui", action="store_true", help="Launch gui application.")
    args = parser.parse_args()

    return args

def run_gui(imdb_scraper):
    app = QGuiApplication(sys.argv)
    app.setWindowIcon(QIcon('images/imdb-icon.png'))

    engine = QQmlApplicationEngine()
    engine.quit.connect(app.quit)
    engine.load('main.qml')

    ctx = engine.rootContext()
    ctx.setContextProperty("imdb", imdb_scraper)

    sys.exit(app.exec())

if __name__ == "__main__":
    args = parse_args()

    imdb_scraper = IMDbScraper()

    if args.recommend:
        print_recommended_movie(imdb_scraper)

    if args.show:
        print_all_movies(imdb_scraper)

    if args.gui:
        run_gui(imdb_scraper)
