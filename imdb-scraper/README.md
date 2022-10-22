# IMDb scraper

An IMDb Top 250 scraper with different functionality.

## Instructions on Windows

- Download and install [Python3](https://www.python.org/downloads/).
- Install virtualenv: `pip install virtualenv`.
- Create a virtual environment: `virtualenv venv`
- Activate the environment: `venv\Scripts\activate`
- If you have issues with execution policies: `Set-ExecutionPolicy Unrestricted -Scope Process`
- Install requirements: `pip install -r requirements.txt`

## Show all Top 250 movies

`python imdb-scraper.py --show`

## Randomly select a movie

`python imdb-scraper.py --random`
