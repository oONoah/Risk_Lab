import pandas as pd
import yfinance as yf

if __package__:
    from ..config import DATA_RAW
else:
    import sys
    from pathlib import Path

    sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
    from risklab.config import DATA_RAW


def fetch_yahoo(
    ticker: str, start: str = "2010-01-01", end: str | None = None
) -> pd.DataFrame:
    """Load Yahoo Finance data from the local cache or download it once."""
    ticker = ticker.strip().upper()
    start_ts = pd.to_datetime(start).normalize()
    end_ts = pd.to_datetime(end).normalize() if end is not None else None

    if end_ts is not None and end_ts <= start_ts:
        raise ValueError("Timehorizon is invalid - end date must be greater than start date")

    cache_end = end_ts if end_ts is not None else pd.Timestamp.today().normalize()
    filename = f"{ticker}_{start_ts:%Y-%m-%d}_{cache_end:%Y-%m-%d}.parquet"
    filepath = DATA_RAW / filename

    if filepath.exists():
        cached = pd.read_parquet(filepath)
        if "Adj Close" in cached.columns:
            return cached

    df_raw = yf.download(
        tickers=ticker,
        start=start_ts,
        end=end_ts,
        auto_adjust=False,
    )
    if df_raw.empty:
        raise ValueError(
            f"Ticker '{ticker}' does not deliver any data - "
            "ticker does not exist or is delisted"
        )

    DATA_RAW.mkdir(parents=True, exist_ok=True)
    df_raw.to_parquet(filepath, engine="pyarrow")
    return df_raw