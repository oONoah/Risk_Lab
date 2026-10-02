import pandas as pd
import pytest

from risklab.data import loader


@pytest.fixture
def market_data() -> pd.DataFrame:
    index = pd.date_range("2026-01-02", periods=3, freq="D")
    return pd.DataFrame(
        {
            "Open": [100.0, 101.0, 102.0],
            "Close": [101.0, 100.5, 103.0],
            "Volume": [1000, 1100, 1200],
        },
        index=index,
    )


def test_fetch_yahoo_uses_existing_cache(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
    market_data: pd.DataFrame,
) -> None:
    monkeypatch.setattr(loader, "DATA_RAW", tmp_path)
    cache_path = tmp_path / "AAPL_2026-01-01_2026-01-10.parquet"
    market_data.to_parquet(cache_path, engine="pyarrow")

    def fail_if_called(**kwargs):
        raise AssertionError("Yahoo Finance darf bei einem Cache-Hit nicht aufgerufen werden")

    monkeypatch.setattr(loader.yf, "download", fail_if_called)

    result = loader.fetch_yahoo("aapl", start="2026-01-01", end="2026-01-10")

    pd.testing.assert_frame_equal(result, market_data, check_freq=False)


def test_fetch_yahoo_downloads_and_caches_data(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
    market_data: pd.DataFrame,
) -> None:
    monkeypatch.setattr(loader, "DATA_RAW", tmp_path)
    calls = []

    def fake_download(**kwargs):
        calls.append(kwargs)
        return market_data

    monkeypatch.setattr(loader.yf, "download", fake_download)

    result = loader.fetch_yahoo(" aapl ", start="2026-01-01", end="2026-01-10")

    cache_path = tmp_path / "AAPL_2026-01-01_2026-01-10.parquet"
    assert calls == [
        {
            "tickers": "AAPL",
            "start": pd.Timestamp("2026-01-01"),
            "end": pd.Timestamp("2026-01-10"),
        }
    ]
    assert cache_path.exists()
    pd.testing.assert_frame_equal(result, market_data)
    pd.testing.assert_frame_equal(
        pd.read_parquet(cache_path), market_data, check_freq=False
    )


def test_fetch_yahoo_rejects_invalid_date_range(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr(loader, "DATA_RAW", tmp_path)
    monkeypatch.setattr(
        loader.yf,
        "download",
        lambda **kwargs: pytest.fail("Yahoo Finance darf nicht aufgerufen werden"),
    )

    with pytest.raises(ValueError, match="end date must be greater"):
        loader.fetch_yahoo("AAPL", start="2026-01-10", end="2026-01-01")


def test_fetch_yahoo_rejects_empty_download(
    monkeypatch: pytest.MonkeyPatch,
    tmp_path,
) -> None:
    monkeypatch.setattr(loader, "DATA_RAW", tmp_path)
    monkeypatch.setattr(loader.yf, "download", lambda **kwargs: pd.DataFrame())

    with pytest.raises(ValueError, match="does not deliver any data"):
        loader.fetch_yahoo("MISSING", start="2026-01-01", end="2026-01-10")
