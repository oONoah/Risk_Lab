import numpy as np
import pandas as pd

def calculate_portfolio_variance(weights: np.ndarray, cov_matrix: np.ndarray) -> float:
    # Expliziter Cast, da das Skalarprodukt von numpy-Arrays einen np.float64 liefert
    return float(weights.T @ cov_matrix @ weights)

class StressTestEngine:
    def __init__(self, weights: np.ndarray, returns: pd.DataFrame):
        self.weights = weights
        self.returns = returns

    def apply_historical_shock(self, start_date: str = "2020-02-01", end_date: str = "2020-03-31") -> float:
        
        # Zeitraum für den COVID-19-Crash angepasst
        stress_window = self.returns.loc[start_date:end_date]
        stress_cov = stress_window.cov().values
        
        return calculate_portfolio_variance(self.weights, stress_cov)