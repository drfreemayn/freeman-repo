
import argparse
import random
import re

import pandas as pd
import requests
from bs4 import BeautifulSoup

TITLE_PATTERN = r"(\w+)\.\n[\s\t]+([\S\s]+)\n\((\w+)"


def scrape_imdb():
    URL = "https://www.imdb.com/chart/top/?ref_=nv_mv_250"
    page = requests.get(URL)
    soup = BeautifulSoup(page.content, "html.parser")
    return soup

def add_title_data(movie_element, movie_dict):
    title_element = movie_element.find("td", class_="titleColumn").text.strip(" \n")

    result = re.match(TITLE_PATTERN, title_element)
    movie_dict["Rank"] = result.group(1)
    movie_dict["Title"] = result.group(2)
    movie_dict["Year"] = result.group(3)
    return movie_dict

def add_rating_data(movie_element, movie_dict):
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

def get_top_250(soup):
    # Extract all movie elements.
    movie_elements = soup.find("tbody", class_="lister-list").find_all("tr")

    # Loop over all movies and extract data.
    imdb_top_250 = []
    for movie_element in movie_elements:
        movie_dict = {}
        movie_dict = add_title_data(movie_element, movie_dict)
        movie_dict = add_rating_data(movie_element, movie_dict)
        imdb_top_250.append(movie_dict)
        
    return imdb_top_250

def select_random_movie(movie_list):
    idx = random.randint(0, 249)
    return movie_list[idx]

def parse_args():
    parser = argparse.ArgumentParser(description="IMDB movie selection.")
    parser.add_argument("--random", action="store_true", help="Select movie randomly.")
    parser.add_argument("--show", action="store_true", help="Show all movies.")
    args = parser.parse_args()

    return args

if __name__ == "__main__":
    args = parse_args()

    soup = scrape_imdb()
    movie_list = get_top_250(soup)

    if args.random:
        movie = select_random_movie(movie_list)
        print("\nThe randomly chosen movie was:\n")
        print(f'# {movie["Rank"]}. {movie["Title"]} ({movie["Year"]}) Rating: {movie["Rating"]}\n')
    
    if args.show:
        imdb_df = pd.DataFrame(movie_list)
        print(imdb_df.to_string(index=False))
