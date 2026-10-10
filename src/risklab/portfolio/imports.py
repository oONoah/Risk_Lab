from pathlib import Path

import pandas as pd


def import_returns_csv(
    path: str | Path,
    *,
    index_col: int | str = 0,
    parse_dates: bool = True,
) -> pd.DataFrame:
    """Load one or more asset return series from a CSV file."""
    input_path = Path(path)
    if not input_path.exists():
        raise FileNotFoundError(f"CSV-Datei wurde nicht gefunden: {input_path}")

    if input_path.suffix.lower() != ".csv":
        raise ValueError("Der Import unterstützt nur .csv-Dateien")

    try:
        returns = pd.read_csv(
            input_path,
            index_col=index_col,
            parse_dates=parse_dates,
        )
    except (OSError, ValueError, TypeError) as error:
        raise ValueError(f"CSV-Datei konnte nicht gelesen werden: {input_path}") from error

    if returns.empty or returns.columns.empty:
        raise ValueError("CSV-Datei muss mindestens eine Return-Spalte enthalten")

    try:
        numeric_returns = returns.astype(float)
    except (TypeError, ValueError) as error:
        raise ValueError("CSV-Datei muss ausschließlich numerische Returns enthalten") from error

    if numeric_returns.dropna(how="all").empty:
        raise ValueError("CSV-Datei muss mindestens einen Return-Wert enthalten")

    return numeric_returns +1
