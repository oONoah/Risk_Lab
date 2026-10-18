from .loader import fetch_yahoo

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

if __package__:
    from ..config import DATA_PROCESSED
else:
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from risklab.config import DATA_PROCESSED


def prepare_returns(
    ticker: str, start: str = "2010-01-01", end: str | None = None
) -> pd.DataFrame:

    df = fetch_yahoo(ticker, start, end)

    if end is None:
        end = str(df.iloc[-1].name)[:10]

    filename = f"PROC_{ticker}_{start}_{end}.parquet"
    filepath = DATA_PROCESSED / filename

    if filepath.exists():
        cached = pq.read_table(filepath).to_pandas(ignore_metadata=True)
        cached["Date"] = pd.to_datetime(cached["Date"].astype("int64"), unit="ms")
        return cached.set_index("Date")

    df = calculate_return(df)

    df.to_parquet(filepath, engine="pyarrow")

    return df

def calculate_return(df: pd.DataFrame) -> pd.DataFrame:
    results = df.copy()   
     
    results["Return"] = (results["Close"] - results["Open"]) / results["Open"]
    results["LogReturn"] = np.log(results["Close"] / results["Close"].shift(1))
    results["RollingVolatility20"] = results["Return"].rolling(window=20).std()
    results["RollingReturn20"] = results["Return"].rolling(window=20).mean()

    return results
