import numpy as np
import pandas as pd

def calculate_portfolio_variance(weights: np.ndarray,
                                 cov_matrix: np.ndarray) -> float:
    return weights.T @ cov_matrix @ weights


class stressEngineTest:
        def _innit__(self,
                        weights: np.ndarray,
                        returns: pd.DataFrame):
                self.weights = weights
                self.returns = returns

        def apply_historical_shock (
                self,
                start_date: str = "2020-03-01",
                end_date: str = "2026-03-31"
                ) -> dict:

                stress_winodw = self.retruns.loc[start_date:end_date]
                stress_cov = stress_winodw.cov().values

                variance_under_stress = calculate_portfolio_variance(self.weights, stress_cov)      
                
                return variance_under_stress

