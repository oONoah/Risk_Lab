import numpy as np
import pandas as pd

from risklab.data import transforms


def test_calculate_log_returns_uses_adjusted_close() -> None:
    prices = pd.DataFrame({"Adj Close": [100.0, 110.0, 99.0]})

    result = transforms.calculate_log_returns(prices)

    expected = np.log(prices["Adj Close"] / prices["Adj Close"].shift(1))
    pd.testing.assert_series_equal(result, expected)


def test_build_portfolio_returns_aligns_fills_and_calculates_log_returns(
    monkeypatch,
) -> None:
    data = {
        "AAPL": pd.DataFrame(
            {"Adj Close": [100.0, 110.0]},
            index=pd.to_datetime(["2026-01-01", "2026-01-03"]),
        ),
        "MSFT": pd.DataFrame(
            {"Adj Close": [200.0, 220.0]},
            index=pd.to_datetime(["2026-01-02", "2026-01-03"]),
        ),
    }
    calls = []

    def fake_fetch(ticker, start, end):
        calls.append((ticker, start, end))
        return data[ticker]

    monkeypatch.setattr(transforms, "fetch_yahoo", fake_fetch)

    result = transforms.build_portfolio_returns(
        ["AAPL", "MSFT"], "2026-01-01", "2026-01-04"
    )

    expected = pd.DataFrame(
        {
            "AAPL": [np.log(110 / 100)],
            "MSFT": [np.log(220 / 200)],
        },
        index=pd.to_datetime(["2026-01-03"], utc=True),
    )
    pd.testing.assert_frame_equal(result, expected)
    assert calls == [
        ("AAPL", "2026-01-01", "2026-01-04"),
        ("MSFT", "2026-01-01", "2026-01-04"),
    ]
