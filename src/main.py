import sys

from risklab import historical_var
from risklab.data import calculate_return, fetch_yahoo, prepare_returns


df = prepare_returns(ticker="AAPL", start="2020-01-01", end="2025-12-31")


print("test commit")
print(historical_var(df["Returns"], 0.9))