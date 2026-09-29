import pandas as pd
import yfinance as yf
import fastparquet

if __package__:
    from .config import DATA_RAW
else:
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from risklab.config import DATA_RAW


def fetch_yahoo(
    ticker: str, start: str = "2010-01-01", end: str | None = None
) -> pd.DataFrame:

    start_ts = pd.to_datetime(start)
    end_ts = pd.to_datetime(end) if end is not None else None

    if end_ts is not None and end_ts <= start_ts:
        raise ValueError("Timehorizon is invalid - end date must be greater than start date")

    df_raw = yf.download(tickers = ticker, start = start, end = end)
    if(df_raw.empty):
        raise ValueError(f"Ticker '{ticker}' does not deliver any data - Ticker does not exisit or is delisted")
    
    print(df_raw.tail(10))

    if end is None:
        end = str(df_raw.iloc[-1].name)[:10]

    filename = f"{ticker}_{start}_{end}.parquet"
    filepath = DATA_RAW / filename

    if filepath.exists():
        return pd.read_parquet(filepath)

    df_raw.to_parquet(filepath)
    return df_raw




fetch_yahoo("AAPL")