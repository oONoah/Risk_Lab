import pandas as pd


def historical_var(
    returns: pd.Series,
    confidence_level: float = 0.95,
    portfolio_value: float = 1.0,
) -> float:
    
    if returns.empty:
        raise ValueError("returns darf nicht leer sein")

    if not 0 < confidence_level < 1:
        raise ValueError("confidence_level muss zwischen 0 und 1 liegen")

    if portfolio_value < 0:
        raise ValueError("portfolio_value darf nicht negativ sein")

    clean_returns = returns.dropna().astype(float)
    if clean_returns.empty:
        raise ValueError("returns muss mindestens eine numerische Beobachtung enthalten")

    losses = -clean_returns
    var = losses.quantile(confidence_level)

    return float(var * portfolio_value)


def expected_shortfall(
    returns: pd.Series,
    confidence_level: float = 0.95,
    portfolio_value: float = 1.0,
) -> float:
    """Calculate historical expected shortfall from a return series."""
    if returns.empty:
        raise ValueError("returns darf nicht leer sein")

    if not 0 < confidence_level < 1:
        raise ValueError("confidence_level muss zwischen 0 und 1 liegen")

    if portfolio_value < 0:
        raise ValueError("portfolio_value darf nicht negativ sein")

    clean_returns = returns.dropna().astype(float)
    if clean_returns.empty:
        raise ValueError("returns muss mindestens eine numerische Beobachtung enthalten")

    losses = -clean_returns
    var = losses.quantile(confidence_level)
    tail_losses = losses[losses >= var]

    return float(tail_losses.mean() * portfolio_value)
