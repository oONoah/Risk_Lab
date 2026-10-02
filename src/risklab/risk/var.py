import pandas as pd



def historical_val(returns:pd.Series,
                   confidence_level: float = 0.95,
                   portfolio_value: float = 1.0,
                   ) -> float:
    