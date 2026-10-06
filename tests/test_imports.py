import pandas as pd
import pytest

from risklab import export_portfolio_returns, import_returns_csv


def test_import_returns_csv_reads_asset_columns(tmp_path) -> None:
    path = tmp_path / "returns.csv"
    expected = pd.DataFrame(
        {"AAPL": [0.01, -0.02], "MSFT": [0.02, 0.01]},
        index=pd.to_datetime(["2026-01-01", "2026-01-02"]),
    )
    expected.to_csv(path)

    result = import_returns_csv(path)

    pd.testing.assert_frame_equal(result, expected)


def test_csv_export_can_be_imported_again(tmp_path) -> None:
    path = tmp_path / "portfolio.csv"
    expected = pd.Series(
        [0.01, -0.02],
        index=pd.to_datetime(["2026-01-01", "2026-01-02"]),
        name="PortfolioReturn",
    )

    export_portfolio_returns(expected, path)

    pd.testing.assert_frame_equal(
        import_returns_csv(path),
        expected.to_frame(),
    )


@pytest.mark.parametrize("filename", ["missing.csv", "returns.txt"])
def test_import_returns_csv_rejects_invalid_files(tmp_path, filename) -> None:
    path = tmp_path / filename

    if path.suffix == ".csv":
        path.write_text("Date,AAPL\n2026-01-01,not-a-number\n", encoding="utf-8")

    with pytest.raises((FileNotFoundError, ValueError)):
        import_returns_csv(path)
