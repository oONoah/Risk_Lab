from pathlib import Path

import pandas as pd

def export_portfolio_returns(returns: pd.Series,
                            path: str | Path
                            ) -> Path:
    output_path = Path(path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    if returns.empty:
        ValueError("returns are empty")

    if output_path.suffix.lower() == ".csv":
        returns.to_csv(output_path, header=True)
    elif output_path.suffix.lower() == ".parquet":
        returns.to_frame().to_parquet()
    else:
        return ValueError("Supported Formats are .csv and .parquet")

    return output_path