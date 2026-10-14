import warnings

import numpy as np

from risklab.portfolio.simulator import price_knockout_option_mc


def test_price_knockout_option_scales_drift_by_timestep() -> None:
    np.random.seed(0)

    with warnings.catch_warnings():
        warnings.simplefilter("error", RuntimeWarning)
        result = price_knockout_option_mc(
            100,
            50,
            200,
            5,
            2,
            steps=252,
            num_simulations=100,
        )

    assert 0.0 <= result <= 200.0
