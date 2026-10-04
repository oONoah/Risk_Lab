import pandas as pd
import pytest

from risklab import expected_shortfall, historical_var


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
