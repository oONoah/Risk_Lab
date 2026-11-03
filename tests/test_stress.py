import numpy as np
import pandas as pd
import pytest

from risklab import StressTestEngine, calculate_portfolio_variance
from risklab.portfolio.returns import covariance_matrix


def test_calculate_portfolio_variance() -> None:
    covariance = np.array([[0.04, 0.01], [0.01, 0.09]])

    assert calculate_portfolio_variance(np.array([0.5, 0.5]), covariance) == pytest.approx(
        0.0375
    )


def test_historical_shock_uses_selected_window() -> None:
    returns = pd.DataFrame(
        {
            "AAPL": [0.10, 0.20, 0.02, 0.04],
            "MSFT": [0.20, 0.40, 0.01, 0.03],
        },
        index=pd.date_range("2020-02-01", periods=4, freq="D"),
    )

    result = StressTestEngine([0.5, 0.5], returns).apply_historical_shock(
        "2020-02-01",
        "2020-02-02",
    )

    assert result == pytest.approx(0.01125)


@pytest.mark.parametrize(
    "returns",
    [
        pd.DataFrame(),
        pd.DataFrame({"AAPL": [0.1]}, index=[0]),
    ],
)
def test_stress_engine_rejects_invalid_returns(returns: pd.DataFrame) -> None:
    with pytest.raises(ValueError):
        StressTestEngine([1.0], returns)


def test_historical_shock_rejects_empty_window() -> None:
    returns = pd.DataFrame(
        {"AAPL": [0.1, 0.2]},
        index=pd.date_range("2020-02-01", periods=2, freq="D"),
    )

    with pytest.raises(ValueError):
        StressTestEngine([1.0], returns).apply_historical_shock(
            "2021-01-01",
            "2021-01-02",
        )


def test_regime_conditional_variance_returns_quantile_regime_covariances() -> None:
    index = pd.date_range("2020-02-01", periods=8, freq="D")
    returns = pd.DataFrame(
        {
            "AAPL": [0.01, 0.02, 0.03, 0.01, 0.02, 0.04, 0.08, 0.10],
            "MSFT": [0.02, 0.01, 0.02, 0.03, 0.01, 0.02, 0.12, 0.15],
        },
        index=index,
    )
    vix = pd.Series(range(1, 9), index=index)

    normal_covariance, stress_covariance = StressTestEngine(
        [0.5, 0.5], returns
    ).regime_conditional_variance(vix, threshold=0.75)

    assert normal_covariance.equals(covariance_matrix(returns.iloc[:6]))
    assert stress_covariance.equals(covariance_matrix(returns.iloc[6:]))


@pytest.mark.parametrize("threshold", [0.0, 1.0])
def test_regime_conditional_variance_rejects_invalid_threshold(
    threshold: float,
) -> None:
    returns = pd.DataFrame(
        {"AAPL": [0.1, 0.2]},
        index=pd.date_range("2020-02-01", periods=2, freq="D"),
    )

    with pytest.raises(ValueError):
        StressTestEngine([1.0], returns).regime_conditional_variance(
            pd.Series([10.0, 20.0], index=returns.index),
            threshold,
        )


@pytest.mark.parametrize(
    "vix_series",
    [
        pd.Series(dtype=float),
        pd.Series([float("nan"), float("inf")]),
        pd.Series(["high", "low"]),
    ],
)
def test_regime_conditional_variance_rejects_invalid_vix(
    vix_series: pd.Series,
) -> None:
    returns = pd.DataFrame(
        {"AAPL": [0.1, 0.2]},
        index=pd.date_range("2020-02-01", periods=2, freq="D"),
    )
    if len(vix_series) == len(returns):
        vix_series.index = returns.index

    with pytest.raises(ValueError):
        StressTestEngine([1.0], returns).regime_conditional_variance(vix_series)


def test_regime_conditional_variance_rejects_missing_dates() -> None:
    returns = pd.DataFrame(
        {"AAPL": [0.1, 0.2]},
        index=pd.date_range("2020-02-01", periods=2, freq="D"),
    )
    vix = pd.Series(
        [10.0, 20.0],
        index=pd.date_range("2021-02-01", periods=2, freq="D"),
    )

    with pytest.raises(ValueError):
        StressTestEngine([1.0], returns).regime_conditional_variance(vix)
