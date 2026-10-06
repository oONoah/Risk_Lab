from pathlib import Path

import pandas as pd


def export_portfolio_returns(returns: pd.Series, path: str | Path) -> Path:

    if returns.empty:
        raise ValueError("returns dürfen nicht leer sein")

    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if output_path.suffix.lower() == ".csv":
        returns.to_csv(output_path, header=True)
    elif output_path.suffix.lower() == ".parquet":
        returns.to_frame().to_parquet(output_path, engine="pyarrow")
    else:
        raise ValueError("Unterstützte Formate sind nur .csv und .parquet")

    return output_path