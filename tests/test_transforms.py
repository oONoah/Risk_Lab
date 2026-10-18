import numpy as np
import pandas as pd
import pytest

from risklab.data.transforms import calculate_return


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
