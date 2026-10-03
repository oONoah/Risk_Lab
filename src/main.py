import sys

from risklab.risk import historical_var
from risklab.data import calculate_return, fetch_yahoo, prepare_returns


df = fetch_yahoo(ticker="AAPL")
df.
print(df.head(10))

