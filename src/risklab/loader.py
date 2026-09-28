import pandas as pd
import yfinance as yf

def fetch_yahoo(ticker:str, start:str = "2010-01-01", end:str | None = None) -> pd.DataFrame:

    start_ts = pd.to_datetime(start)
    end_ts = pd.to_datetime(end)

    if (end_ts <= start_ts):
        raise ValueError("Timehorizon is invalid - end date must be greater than start date")

    DATA_RAW = yf.download(tickers = ticker, start = start, end = end)
    if(DATA_RAW.empty):
        print("Data is unavailabile - check Ticker and Timehorizon")

        raise ValueError(f"Ticker '{ticker}' does not deliver any data - Ticker does not exisit or is delisted")


fetch_yahoo("AAPL",start = "2026-02-01", end="2026-04-01")