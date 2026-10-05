import pandas as pd
import pytest

from risklab import portfolio_returns


def test_portfolio_returns_apply_weights() -> None:
    asset_returns = pd.DataFrame(
        {
            "AAPL": [0.10, 0.00],
            "MSFT": [0.00, 0.20],
        }
    )

    result = portfolio_returns(asset_returns, {"AAPL": 0.6, "MSFT": 0.4})

    pd.testing.assert_series_equal(
        result,
        pd.Series([0.06, 0.08], name="PortfolioReturn"),
    )


def test_portfolio_returns_drop_incomplete_rows() -> None:
    asset_returns = pd.DataFrame(
        {"AAPL": [0.10, None, 0.03], "MSFT": [0.00, 0.20, 0.01]}
    )

    result = portfolio_returns(asset_returns, [0.5, 0.5])

    pd.testing.assert_series_equal(
        result,
        pd.Series([0.05, 0.02], index=[0, 2], name="PortfolioReturn"),
    )


@pytest.mark.parametrize(
    "weights",
    [
        [1.0],
        [0.7, 0.7],
        {"AAPL": 1.0},
        {"AAPL": 0.5, "MSFT": 0.5, "SPY": 0.0},
    ],
)
def test_portfolio_returns_reject_invalid_weights(weights) -> None:
    asset_returns = pd.DataFrame({"AAPL": [0.1], "MSFT": [0.2]})

    with pytest.raises(ValueError):
        portfolio_returns(asset_returns, weights)
