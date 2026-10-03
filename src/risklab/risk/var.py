import pandas as pd



def historical_var(df:pd.Series,
                   confidence_level: float = 0.95,
                   portfolio_value: float = 1.0,
                   ) -> float:

    if ("Return" not in df.columns):
        df["Return"] = (df["Close"] - df["Open"]) / df["Open"]

    df.sort_values("Return", ascending=False)
