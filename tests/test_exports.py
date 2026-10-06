import pandas as pd
import pytest

from risklab import export_portfolio_returns


@pytest.fixture
def portfolio_returns() -> pd.Series:
    return pd.Series(
        [0.01, -0.02],
        index=pd.to_datetime(["2026-01-01", "2026-01-02"]),
        name="PortfolioReturn",
    )


def test_export_portfolio_returns_writes_csv(
    tmp_path,
    portfolio_returns: pd.Series,
) -> None:
    output_path = tmp_path / "nested" / "portfolio.csv"

    result = export_portfolio_returns(portfolio_returns, output_path)

    assert result == output_path
    assert output_path.exists()
    pd.testing.assert_series_equal(
        pd.read_csv(output_path, index_col=0, parse_dates=True)["PortfolioReturn"],
        portfolio_returns,
    )


def test_export_portfolio_returns_writes_parquet(
    tmp_path,
    portfolio_returns: pd.Series,
) -> None:
    output_path = tmp_path / "nested" / "portfolio.parquet"

    result = export_portfolio_returns(portfolio_returns, output_path)

    assert result == output_path
    assert output_path.exists()
    pd.testing.assert_frame_equal(
        pd.read_parquet(output_path),
        portfolio_returns.to_frame(),
    )


@pytest.mark.parametrize("suffix", [".json", ".txt", ""])
def test_export_portfolio_returns_rejects_unsupported_format(
    tmp_path,
    portfolio_returns: pd.Series,
    suffix: str,
) -> None:
    with pytest.raises(ValueError, match="Unterstützte Formate"):
        export_portfolio_returns(
            portfolio_returns,
            tmp_path / f"portfolio{suffix}",
        )


def test_export_portfolio_returns_rejects_empty_series(tmp_path) -> None:
    with pytest.raises(ValueError, match="nicht leer"):
        export_portfolio_returns(
            pd.Series(dtype=float, name="PortfolioReturn"),
            tmp_path / "portfolio.csv",
        )
