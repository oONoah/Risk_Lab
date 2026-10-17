from pathlib import Path

import numpy as np
import pytest


@pytest.fixture
def simulated_portfolio() -> tuple[np.ndarray, np.ndarray]:
    data_path = Path(__file__).parent / "data" / "simulated_portfolio.npz"

    with np.load(data_path) as data:
        returns = data["returns"].copy()
        weights = data["weights"].copy()

    return returns, weights
