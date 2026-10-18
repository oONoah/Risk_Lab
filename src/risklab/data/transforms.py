from .loader import fetch_yahoo

import numpy as np
import pandas as pd
import pyarrow.parquet as pq

TRADING_DAYS_PER_YEAR = 252

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
        if "Adj Close" in cached.columns:
            cached["Date"] = pd.to_datetime(cached["Date"].astype("int64"), unit="ms")
            return cached.set_index("Date")

    df = calculate_return(df)

    df.to_parquet(filepath, engine="pyarrow")

    return df

def calculate_return(df: pd.DataFrame) -> pd.DataFrame:
    results = df.copy()
    if "Adj Close" not in results.columns:
        raise ValueError(
            "Historische Renditen benötigen eine 'Adj Close'-Spalte."
        )

    adjusted_close = results["Adj Close"]
    if isinstance(adjusted_close, pd.DataFrame):
        if adjusted_close.shape[1] != 1:
            raise ValueError("'Adj Close' muss genau einen Ticker enthalten.")
        adjusted_close = adjusted_close.iloc[:, 0]

    results["Return"] = adjusted_close.pct_change()
    results["LogReturn"] = np.log(adjusted_close / adjusted_close.shift(1))
    results["RollingVolatility20"] = (
        results["LogReturn"].rolling(window=20).std()
        * np.sqrt(TRADING_DAYS_PER_YEAR)
    )
    results["RollingReturn20"] = results["Return"].rolling(window=20).mean()

    return results


def calculate_log_returns(
    df: pd.DataFrame, price_column: str = "Adj Close"
) -> pd.Series:
    """Berechnet logarithmische Close-to-Close-Renditen einer Preisreihe."""
    prices = _single_price_series(df, price_column)
    return np.log(prices / prices.shift(1))


def _single_price_series(df: pd.DataFrame, price_column: str) -> pd.Series:
    prices = df[price_column]
    if isinstance(prices, pd.DataFrame):
        if prices.shape[1] != 1:
            raise ValueError(f"'{price_column}' muss genau eine Preisreihe enthalten.")
        prices = prices.iloc[:, 0]

    return prices


def build_portfolio_returns(
    tickers: list[str], start: str, end: str | None = None
) -> pd.DataFrame:
    """Lädt mehrere Ticker und erstellt eine synchronisierte Log-Renditenmatrix."""
    price_series: dict[str, pd.Series] = {}

    for ticker in tickers:
        df_raw = fetch_yahoo(ticker, start, end)
        df_raw = df_raw.copy()
        df_raw.index = pd.to_datetime(df_raw.index, utc=True).normalize()
        price_series[ticker] = _single_price_series(df_raw, "Adj Close")

    portfolio_prices = pd.DataFrame(price_series).ffill()
    log_returns = np.log(portfolio_prices / portfolio_prices.shift(1))

    return log_returns.dropna()
