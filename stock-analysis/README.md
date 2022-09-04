# Stock analysis

This is a collection of scripts to analyse stocks.

## Instructions

- Download and install [Python3](https://www.python.org/downloads/).
- Install virtualenv: `pip install virtualenv`.
- Create a virtual environment: `virtualenv venv`
- Activate the environment: `venv\Scripts\activate`
- If you have issues with execution policies: `Set-ExecutionPolicy Unrestricted -Scope Process`
- Install requirements: `pip install -r requirements.txt`

## Tickers

Store all available stock tickers to `tickers.csv`:

`python stock-analysis.py --tickers`

## Report

Store a stock analysis report to ` stocks.csv` based on tickers in `tickers.yaml`:

`python stock-analysis.py --report --out_csv stocks.csv`

## Technicals

Store a technical analysis report to `technicals.csv` based on tickers in `tickers.yaml`:

`python stock-analysis.py --technicals --out_csv technicals.csv`

## Price data

Store all available price data to based on tickers in `tickers.yaml` or tickers specified by `in_csv`:

- **yaml**: `python stock-analysis.py --price`
- **csv**: `python stock-analysis.py --price --in_csv tickers.csv`
