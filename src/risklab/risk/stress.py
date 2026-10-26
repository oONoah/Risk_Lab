import numpy as np
import pandas as pd

from risklab.portfolio.returns import covariance_matrix, portfolio_variance


def calculate_portfolio_variance(
    weights: np.ndarray,
    cov_matrix: np.ndarray,
) -> float:
    """Calculate portfolio variance from array-like weights and covariance."""
    weights_array = np.asarray(weights, dtype=float)
    covariance_array = np.asarray(cov_matrix, dtype=float)

    if weights_array.ndim != 1:
        raise ValueError("weights müssen ein eindimensionales Array sein")
    if covariance_array.ndim != 2 or covariance_array.shape[0] != covariance_array.shape[1]:
        raise ValueError("cov_matrix muss eine quadratische Matrix sein")
    if covariance_array.shape[0] != len(weights_array):
        raise ValueError("weights und cov_matrix müssen dieselbe Dimension haben")
    if not np.isfinite(weights_array).all() or not np.isfinite(covariance_array).all():
        raise ValueError("weights und cov_matrix müssen endliche Werte enthalten")

    return float(weights_array @ covariance_array @ weights_array)


def calculate_absorption_rate(cov_matrix: np.ndarray) -> float:
    eigenvalues, eigenvectors = np.linalg.eigh(cov_matrix)

    max_eigenvalue = eigenvalues[-1]
    total_variance = np.sum(eigenvalues)

    return float(max_eigenvalue/total_variance)    




class StressTestEngine:
    def __init__(self, weights: np.ndarray, returns: pd.DataFrame):
        if returns.empty:
            raise ValueError("returns darf nicht leer sein")
        if not isinstance(returns.index, pd.DatetimeIndex):
            raise ValueError("returns benötigt einen DatetimeIndex")

        self.weights = np.asarray(weights, dtype=float)
        if self.weights.ndim != 1 or len(self.weights) != len(returns.columns):
            raise ValueError("Anzahl der weights muss der Asset-Anzahl entsprechen")
        if not np.isfinite(self.weights).all():
            raise ValueError("weights müssen endlich sein")
        self.returns = returns

    def apply_historical_shock(
        self,
        start_date: str = "2020-02-01",
        end_date: str = "2020-03-31",
    ) -> float:
        """Return portfolio variance estimated from a historical stress window."""
        stress_window = self.returns.loc[start_date:end_date]
        if len(stress_window) < 2:
            raise ValueError("Stressfenster muss mindestens zwei Beobachtungen enthalten")

        stress_covariance = covariance_matrix(stress_window)
        return portfolio_variance(stress_covariance, self.weights)


    def regime_conditional_variance() -> float:
        print() 
        #missing test + implementation 

    def analyze_regime_breakdown(
        self,
        vix_series: pd.Series,
        threshold: float = 0.95
    ) -> dict:
        cov_normal, cov_stress = self.regime_conditional_variance(vix_series, threshold)    