import numpy as np
import pandas as pd
import pytest

from risklab import (
    christoffersen,
    expected_shortfall,
    historical_var,
    kupiec_pof,
)


@pytest.mark.parametrize(
    ("failures", "expected_lr", "expected_rejection"),
    [
        (0, -2 * 100 * np.log(0.99), False),
        (100, -2 * 100 * np.log(0.01), True),
    ],
)
def test_kupiec_pof_handles_boundary_failure_counts(
    failures: int,
    expected_lr: float,
    expected_rejection: bool,
) -> None:
    result = kupiec_pof(failures, observations=100)

    assert result["lr_pof"] == pytest.approx(expected_lr)
    assert np.isfinite(result["p_value"])
    assert result["is_rejected"] is expected_rejection


def test_christoffersen_returns_nan_for_hits_without_failures() -> None:
    result = christoffersen(np.zeros(5, dtype=int))

    assert np.isnan(result["lr_ind"])
    assert np.isnan(result["p_value"])
    assert result["is_rejected"] is False


def test_christoffersen_calculates_independence_statistic() -> None:
    hits = np.array([0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1])

    result = christoffersen(hits)

    assert result["lr_ind"] == pytest.approx(0.1303319159)
    assert result["p_value"] == pytest.approx(0.7180881451)
    assert result["is_rejected"] is False


def test_expected_shortfall_averages_losses_in_var_tail() -> None:
    returns = pd.Series([0.10, 0.02, -0.10, -0.20])

    assert historical_var(returns, confidence_level=0.75) == pytest.approx(0.125)
    assert expected_shortfall(returns, confidence_level=0.75) == pytest.approx(0.20)


def test_expected_shortfall_scales_with_portfolio_value() -> None:
    returns = pd.Series([-0.10, -0.20, 0.05, 0.10])

    assert expected_shortfall(
        returns,
        confidence_level=0.75,
        portfolio_value=100_000,
    ) == pytest.approx(20_000)


@pytest.mark.parametrize(
    ("returns", "confidence_level", "portfolio_value"),
    [
        (pd.Series(dtype=float), 0.95, 1.0),
        (pd.Series([float("nan")]), 0.95, 1.0),
        (pd.Series([0.1]), 0.0, 1.0),
        (pd.Series([0.1]), 1.0, 1.0),
        (pd.Series([0.1]), 0.95, -1.0),
    ],
)
def test_expected_shortfall_rejects_invalid_input(
    returns: pd.Series,
    confidence_level: float,
    portfolio_value: float,
) -> None:
    with pytest.raises(ValueError):
        expected_shortfall(returns, confidence_level, portfolio_value)
