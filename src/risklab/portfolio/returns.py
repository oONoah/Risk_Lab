from collections.abc import Mapping, Sequence

import numpy as np
import pandas as pd


def portfolio_returns(
    asset_returns: pd.DataFrame,
    weights: Mapping[str, float] | Sequence[float],
) -> pd.Series:
    """Calculate weighted portfolio returns from aligned asset returns.

    Rows containing a missing asset return are excluded so every portfolio
    return uses the same set of assets
    """
    if asset_returns.empty:
        raise ValueError("asset_returns darf nicht leer sein")

    if asset_returns.columns.empty:
        raise ValueError("asset_returns muss mindestens ein Asset enthalten")

    if isinstance(weights, Mapping):
        missing = [column for column in asset_returns.columns if column not in weights]
        extra = [column for column in weights if column not in asset_returns.columns]
        if missing or extra:
            raise ValueError(
                f"weights müssen exakt zu den Assets passen; fehlend={missing}, "
                f"unbekannt={extra}"
            )
        weight_values = np.asarray(
            [weights[column] for column in asset_returns.columns],
            dtype=float,
        )
    else:
        weight_values = np.asarray(weights, dtype=float)
        if weight_values.ndim != 1 or len(weight_values) != len(asset_returns.columns):
            raise ValueError("Anzahl der weights muss der Asset-Anzahl entsprechen")

    if not np.isfinite(weight_values).all():
        raise ValueError("weights müssen endlich sein")

    if not np.isclose(weight_values.sum(), 1.0):
        raise ValueError("weights müssen sich zu 1 summieren")

    try:
        numeric_returns = asset_returns.astype(float)
    except (TypeError, ValueError) as error:
        raise ValueError("asset_returns müssen numerische Werte enthalten") from error

    clean_returns = numeric_returns.dropna(how="any")
    if clean_returns.empty:
        raise ValueError("asset_returns müssen mindestens eine vollständige Zeile enthalten")

    result = clean_returns.mul(weight_values, axis="columns").sum(axis="columns")
    result.name = "PortfolioReturn"
    return result
