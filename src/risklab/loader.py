import pandas as pd
import yfinance as yf

def fetch_yahoo(ticker:str, start:str = "01-01-2010", end:str | None = None) -> pd.DataFrame:
    DATA_RAW = yf.download