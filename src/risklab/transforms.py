from ast import literal_eval

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

if __package__:
    from .config import DATA_PROCESSED, DATA_RAW
else:
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from risklab.config import DATA_PROCESSED, DATA_RAW


def prepare_returns(
    ticker: str, start: str = "2010-01-01", end: str | None = None
) -> pd.DataFrame:
    files = [
        file.name
        for file in DATA_RAW.iterdir()
        if file.is_file()
        and file.suffix == ".parquet"
        and file.name.startswith(ticker)
    ]

    if not files:
        raise FileNotFoundError(
            f"Keine Parquet-Datei für {ticker} in {DATA_RAW} gefunden."
        )

    df = pq.read_table(DATA_RAW / files[0]).to_pandas(ignore_metadata=True)
    df["Date"] = pd.to_datetime(df["Date"].astype("int64"), unit="ms")
    df = df.set_index("Date")

    df.columns = [
        literal_eval(column)[0] if isinstance(column, str) and column.startswith("(") else column
        for column in df.columns
    ]

    df["Return"] = (df["Close"] - df["Open"]) / df["Open"]
    df["LogReturn"] = np.log(df["Close"] / df["Close"].shift(1))
    df["RollingVolatility20"] = df["Return"].rolling(window=20).std()
    df["RollingReturn20"] = df["Return"].rolling(window=20).mean()
    anualized_volatility = df["Return"].std() * np.sqrt(252)

    print(df.tail(10))


    if end is None:
        end = str(df.iloc[-1].name)[:10]

    filename = f"PROC_{ticker}_{start}_{end}.parquet"
    filepath = DATA_PROCESSED / filename

    if filepath.exists():
        cached = pq.read_table(filepath).to_pandas(ignore_metadata=True)
        cached["Date"] = pd.to_datetime(cached["Date"].astype("int64"), unit="ms")
        return cached.set_index("Date")

    df.to_parquet(filepath, engine="pyarrow")

    return df

prepare_returns("AAPL")