import argparse as ap
import json
import os
from pathlib import Path
from typing import List

import pandas as pd
import yaml
import yfinance as yf
from pyfinviz.quote import Quote
from pyfinviz.screener import Screener

# Current number of pages on finviz.
MAX_NUM_PAGES = 428

INFO_LIST = {
    "longName": "Namn",
    "currency": "Valuta",
    "previousClose": "Kurs",
    "marketCap": "Market Cap (B)",
    "enterpriseValue": "EV (B)",
    "enterpriseToRevenue": "EV/R",
    "enterpriseToEbitda": "EV/EBIDTA",
    "priceToSalesTrailing12Months": "P/S",
    "trailingPE": "P/E",
    "forwardPE": "P/E (forward)",
    "pegRatio": "PEG",
    "dividendYield": "Direktavkastning (%)",
    "trailingEps": "EPS",
    "forwardEps": "EPS (forward)",
    "shortRatio": "Short ratio (%)",
    "targetMedianPrice": "Riktkurs (median)",
    "targetMeanPrice": "Riktkurs (medel)",
    "targetHighPrice": "Riktkurs (high)",
}


def get_tickers_from_yaml() -> List[str]:
    current_dir = Path(__file__).parent.resolve()
    with open(current_dir / "tickers.yaml", "r") as stream:
        ticker_dict = yaml.safe_load(stream)
    return ticker_dict["tickers"]


def get_tickers_from_csv(in_csv: Path) -> List[str]:
    ticker_df = pd.read_csv(in_csv, sep="\t")
    return ticker_df["Ticker"]


def generate_csv_report(out_csv: Path, debug: bool = False) -> None:
    if not out_csv:
        current_dir = Path(__file__).parent.resolve()
        out_csv = current_dir / "stocks.csv"

    # Setup tickers.
    ticker_list = get_tickers_from_yaml()
    ticker_str = " ".join(ticker_list)
    tickers = yf.Tickers(ticker_str)

    # Initialize empty dataframe with valid columns.
    merged_df = pd.DataFrame(columns=INFO_LIST.keys())

    # Loop over all tickers.
    print("Analysing ticker:")
    for symbol, ticker in tickers.tickers.items():

        # Debug info.
        print(symbol)
        if debug:
            with open(f"stock-{symbol}.txt", "w") as txtfile:
                json.dump(ticker.info, txtfile, indent=4)

        # Extract ticker info and valid columns.
        df = pd.DataFrame([ticker.info])
        cols = list(set(df.columns) & set(merged_df.columns))

        # Select valid columns.
        sel_df = df[cols]

        # Add current ticker data to df.
        merged_df = pd.concat([merged_df, sel_df])

    # Post-process some columns.
    merged_df[["marketCap", "enterpriseValue"]] = merged_df[
        ["marketCap", "enterpriseValue"]
    ] * 10 ** (-9)
    merged_df["dividendYield"] = merged_df["dividendYield"] * 100

    # Change column names.
    merged_df.columns = INFO_LIST.values()
    merged_df = merged_df.fillna(0.0)

    # Write to disk.
    merged_df.to_csv(out_csv, index=False, sep="\t", decimal=",", float_format="%.2f")
    print(f"Results stored to {out_csv}.")


def get_stock_tickers(num_pages: int, out_csv: Path) -> None:
    if not out_csv:
        current_dir = Path(__file__).parent.resolve()
        out_csv = current_dir / "tickers.csv"

    # Use screener to retrieve num_pages of Tickers from finviz.
    page_list = list(range(0, num_pages))
    # Only retrieve stocks.
    options = [Screener.IndustryOption.STOCKS_ONLY_EX_FUNDS]
    screener = Screener(filter_options=options, pages=page_list)
    columns = [
        "Ticker",
        "Company",
        "Sector",
        "Industry",
        "Country",
        "MarketCap",
        "PE",
        "Volume",
    ]
    tickers_df = pd.DataFrame(columns=columns)
    for i in page_list:
        if i == 1:
            # Results were repeated for i = [0, 1].
            continue
        curr_df = screener.data_frames[i]
        # Remove all tickers without market cap.
        sel_df = curr_df.loc[curr_df["MarketCap"] != "-"]
        tickers_df = pd.concat([tickers_df, sel_df[columns]])

    # Drop potential duplicates if too many pages were selected.
    tickers_df = tickers_df.drop_duplicates()

    # Write tickers to csv.
    tickers_df.to_csv(out_csv, index=False, sep="\t")


def get_stock_technicals(out_csv: Path) -> None:
    # Determine path for storage.
    if not out_csv:
        current_dir = Path(__file__).parent.resolve()
        out_csv = current_dir / "technicals.csv"

    ticker_list = get_tickers_from_yaml()
    technical_df = pd.DataFrame()
    for ticker in ticker_list:
        quote = Quote(ticker=ticker)
        if quote.exists:
            ticker_dict = {
                "Ticker": [quote.ticker],
                "Company": [quote.company_name],
                "Sector": [quote.sectors[0]],
                "Industry": [quote.sectors[1]],
                "Country": [quote.sectors[2]],
            }
            ticker_df = pd.DataFrame(ticker_dict)
            # Other variables: outer_ratings_df, outer_news_df, income_statement_df, insider_trading_df
            merged_df = pd.concat([ticker_df, quote.fundamental_df], axis=1)
            technical_df = pd.concat([technical_df, merged_df])

    # Write tickers to csv.
    technical_df.to_csv(out_csv, index=False, sep="\t")


def get_price_data(in_csv) -> None:
    current_dir = Path(__file__).parent.resolve()
    price_dir = current_dir / "price_data"
    os.makedirs(price_dir, exist_ok=True)

    if not in_csv:
        ticker_list = get_tickers_from_yaml()
    else:
        ticker_list = get_tickers_from_csv(in_csv)
    ticker_str = " ".join(ticker_list)
    all_tickers_df = yf.download(ticker_str, interval="1d")
    for ticker in ticker_list:
        # Select all columns for ticker.
        ticker_df = all_tickers_df.iloc[
            :, all_tickers_df.columns.get_level_values(1) == ticker
        ]
        # Drop rows without data (i.e. containing NaN).
        ticker_df = ticker_df.dropna()
        # Reduce df to single index instead of multi-index before storage.
        new_columns = ticker_df.columns.get_level_values(0)
        index = ticker_df.index
        ticker_df = pd.DataFrame(ticker_df.values, columns=new_columns, index=index)

        # Write tickers to csv.
        price_csv = price_dir / f"{ticker}.csv"
        ticker_df.to_csv(price_csv, index=True, sep="\t")


def parse_args() -> ap.Namespace:
    parser = ap.ArgumentParser(description="Stock analysis script.")
    parser.add_argument(
        "--tickers", action="store_true", help="Store all stock tickers to csv."
    )
    parser.add_argument(
        "--num_pages",
        default=MAX_NUM_PAGES,
        type=int,
        help="Number of pages of tickers to scrape. Default will take a while.",
    )
    parser.add_argument("--report", action="store_true", help="Generate csv report.")
    parser.add_argument(
        "--technicals", action="store_true", help="Generate technical csv report."
    )
    parser.add_argument("--price", action="store_true", help="Generate price data.")
    parser.add_argument(
        "--in_csv",
        "-i",
        type=Path,
        default=None,
        help="Input file name.",
    )
    parser.add_argument(
        "--out_csv",
        "-o",
        type=Path,
        default=None,
        help="Output file name.",
    )
    parser.add_argument(
        "--debug", action="store_true", help="Write debug information to disk."
    )
    args = parser.parse_args()

    return args


if __name__ == "__main__":
    args = parse_args()
    if args.tickers:
        get_stock_tickers(args.num_pages, args.out_csv)
    if args.report:
        generate_csv_report(args.out_csv, args.debug)
    if args.technicals:
        get_stock_technicals(args.out_csv)
    if args.price:
        get_price_data(args.in_csv)
