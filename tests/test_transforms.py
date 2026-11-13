import numpy as np
import pandas as pd
import pytest

from risklab.data.transforms import calculate_return, prepare_returns


def test_calculate_return_uses_adjusted_close_and_annualizes_log_volatility() -> None:
    adjusted_close = pd.Series(
        np.arange(100.0, 122.0),
        index=pd.date_range("2026-01-01", periods=22, freq="D"),
        name="Adj Close",
    )
    data = pd.DataFrame({"Open": 1.0, "Close": 1.0, "Adj Close": adjusted_close})

    result = calculate_return(data)
    expected_return = adjusted_close.pct_change()
    expected_log_return = np.log(adjusted_close / adjusted_close.shift(1))
    expected_volatility = (
        expected_log_return.rolling(20).std() * np.sqrt(252)
    )

    pd.testing.assert_series_equal(result["Return"], expected_return)
    pd.testing.assert_series_equal(result["LogReturn"], expected_log_return)
    pd.testing.assert_series_equal(
        result["RollingVolatility20"], expected_volatility
    )


def test_calculate_return_requires_adjusted_close() -> None:
    with pytest.raises(ValueError, match="Adj Close"):
        calculate_return(pd.DataFrame({"Close": [100.0, 101.0]}))


def test_prepare_returns_fetches_calculates_and_caches_data(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    data = pd.DataFrame(
        {"Adj Close": [100.0, 110.0]},
        index=pd.date_range("2026-01-01", periods=2, freq="D"),
    )
    calls = []

    def fake_fetch(ticker: str, start: str, end: str | None) -> pd.DataFrame:
        calls.append((ticker, start, end))
        return data

    monkeypatch.setattr("risklab.data.transforms.fetch_yahoo", fake_fetch)
    monkeypatch.setattr("risklab.data.transforms.DATA_PROCESSED", tmp_path)

    result = prepare_returns("AAPL", start="2026-01-01", end="2026-01-02")

    assert calls == [("AAPL", "2026-01-01", "2026-01-02")]
    assert (tmp_path / "PROC_AAPL_2026-01-01_2026-01-02.parquet").exists()
    assert result["Return"].iloc[1] == pytest.approx(0.1)
    assert result["LogReturn"].iloc[1] == pytest.approx(np.log(1.1))
