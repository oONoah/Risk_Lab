from pathlib import Path

from risklab import (
    covariance_matrix,
    import_returns_csv,
    portfolio_variance,
)

returns = import_returns_csv(
    Path("data/simulated/example_portfolio_returns.csv")
)

weights = {
    "AAPL": 0.40,
    "MSFT": 0.30,
    "GLD": 0.20,
    "TLT": 0.10,
}

covariance = covariance_matrix(returns)
variance = portfolio_variance(covariance, weights)
volatility = variance**0.5

print(returns)
print(covariance)
print(f"Portfolio variance: {variance:.12f}")
print(f"Portfolio volatility: {volatility:.12f}")