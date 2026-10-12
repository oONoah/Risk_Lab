import pandas as pd
import pytest

from risklab import covariance_matrix, portfolio_returns, portfolio_variance
from risklab.portfolio.returns import covariance_matrix, portfolio_variance


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


def test_portfolio_returns_preserve_asset_column_order_for_mapping() -> None:
    asset_returns = pd.DataFrame(
        {"MSFT": [0.20], "AAPL": [0.10]},
    )

    result = portfolio_returns(
        asset_returns,
        {"AAPL": 0.25, "MSFT": 0.75},
    )

    assert result.iloc[0] == pytest.approx(0.175)


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


def test_covariance_matrix_calculates_sample_covariance() -> None:
    asset_returns = pd.DataFrame(
        {
            "AAPL": [1.0, 2.0, 3.0],
            "MSFT": [2.0, 4.0, 8.0],
        }
    )

    result = covariance_matrix(asset_returns)

    expected = pd.DataFrame(
        [[1.0, 3.0], [3.0, 28.0 / 3.0]],
        index=["AAPL", "MSFT"],
        columns=["AAPL", "MSFT"],
    )
    pd.testing.assert_frame_equal(result, expected)


def test_covariance_matrix_uses_complete_rows_only() -> None:
    asset_returns = pd.DataFrame(
        {
            "AAPL": [1.0, None, 3.0],
            "MSFT": [2.0, 4.0, 8.0],
        }
    )

    result = covariance_matrix(asset_returns)

    expected = pd.DataFrame(
        [[2.0, 6.0], [6.0, 18.0]],
        index=["AAPL", "MSFT"],
        columns=["AAPL", "MSFT"],
    )
    pd.testing.assert_frame_equal(result, expected)


@pytest.mark.parametrize(
    "weights",
    [
        {"AAPL": 0.25, "MSFT": 0.75},
        [0.25, 0.75],
    ],
)
def test_portfolio_variance_combines_weights_and_covariance(weights) -> None:
    covariance = pd.DataFrame(
        [[1.0, 3.0], [3.0, 9.0]],
        index=["AAPL", "MSFT"],
        columns=["AAPL", "MSFT"],
    )

    result = portfolio_variance(covariance, weights)

    assert result == pytest.approx(6.25)


def test_portfolio_variance_aligns_mapping_weights_to_columns() -> None:
    covariance = pd.DataFrame(
        [[1.0, 3.0], [3.0, 9.0]],
        index=["AAPL", "MSFT"],
        columns=["AAPL", "MSFT"],
    )

    result = portfolio_variance(covariance, {"MSFT": 0.75, "AAPL": 0.25})

    assert result == pytest.approx(6.25)


def test_portfolio_variance_is_available_from_public_api() -> None:
    covariance = pd.DataFrame(
        [[0.04, 0.01], [0.01, 0.09]],
        columns=["AAPL", "MSFT"],
        index=["AAPL", "MSFT"],
    )

    assert portfolio_variance(covariance, [0.5, 0.5]) == pytest.approx(0.0375)
    assert covariance_matrix(
        pd.DataFrame({"AAPL": [0.1, 0.2], "MSFT": [0.2, 0.4]})
    ).shape == (2, 2)


@pytest.mark.parametrize(
    "covariance",
    [
        pd.DataFrame(),
        pd.DataFrame([[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]]),
        pd.DataFrame([[1.0, float("nan")], [0.0, 1.0]]),
    ],
)
def test_portfolio_variance_rejects_invalid_covariance(
    covariance: pd.DataFrame,
) -> None:
    with pytest.raises(ValueError):
        portfolio_variance(covariance, [0.5, 0.5])


@pytest.mark.parametrize(
    "weights",
    [
        [1.0],
        [0.5, 0.5, 0.0],
        {"AAPL": 1.0},
        {"AAPL": 0.5, "MSFT": 0.5, "SPY": 0.0},
    ],
)
def test_portfolio_variance_rejects_weights_with_wrong_assets(weights) -> None:
    covariance = pd.DataFrame(
        [[1.0, 3.0], [3.0, 9.0]],
        index=["AAPL", "MSFT"],
        columns=["AAPL", "MSFT"],
    )

    with pytest.raises(ValueError):
        portfolio_variance(covariance, weights)
