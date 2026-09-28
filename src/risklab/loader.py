import pandas as pd
import yfinance as yf

def fetch_yahoo(ticker:str, start:str = "2010-01-01", end:str | None = None) -> pd.DataFrame:
    DATA_RAW = yf.download(tickers = ticker, start = start, end = end)
    print(DATA_RAW.head(10))

fetch_yahoo("AAPL",end="2026-01-01")