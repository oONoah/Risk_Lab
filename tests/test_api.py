import risklab


def test_public_api_exports_core_functions() -> None:
    assert risklab.fetch_yahoo is not None
    assert risklab.prepare_returns is not None
    assert risklab.calculate_return is not None
    assert risklab.historical_var is not None
