import pandas as pd

pd.set_option('display.max_columns', None)



def historical_var(df:pd.Series,
                   confidence_level: float = 0.95,
                   portfolio_value: float = 1.0,
                   ) -> float:

    if df.empty:
        raise ValueError("df darf nicht leer sein")

    if not 0 < confidence_level < 1:
        raise ValueError("confidence_level muss zwischen 0 und 1 liegen")

    if portfolio_value < 0:
        raise ValueError("portfolio_value darf nicht negativ sein")

    df = df.dropna().astype(float)

    var = -df["Returns"].quantile(confidence_level)

    return var * portfolio_value
