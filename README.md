RiskLab/
├── README.md
├── pyproject.toml / requirements.txt
├── .gitignore
│
├── data/
│   ├── raw/              # Unmodified market data (Yahoo, Quandl, TAQ)
│   ├── processed/        # Cleaned returns, aligned panels, factors
│   └── simulated/        # Monte Carlo or GBM synthetic data
│
├── src/
│   ├── risklab/          # Main Python package
│   │   ├── __init__.py
│   │   ├── config.py     # Central config (paths, constants)
│   │   ├── data/
│   │   │   ├── loader.py         # Fetching, caching, cleaning
│   │   │   ├── transforms.py     # Returns, resampling, winsorizing
│   │   │   └── calendars.py       # Business calendars, holidays
│   │   │
│   │   ├── factors/
│   │   │   ├── factor_store.py    # Factor registry
│   │   │   ├── volatility.py      # EWMA, GARCH
│   │   │   └── risk_factors.py    # Beta, SMB/HML, carry, etc.
│   │   │
│   │   ├── risk/
│   │   │   ├── var.py             # Historical, parametric, MC VaR
│   │   │   ├── es.py              # Expected Shortfall
│   │   │   ├── backtesting.py     # Kupiec, Christoffersen
│   │   │   └── stress.py          # Shock scenarios, regime tests
│   │   │
│   │   ├── portfolio/
│   │   │   ├── allocation.py      # MinVar, RiskParity, Kelly
│   │   │   ├── optimizer.py       # Convex optimization, constraints
│   │   │   └── simulator.py       # Portfolio-level MC simulation
│   │   │
│   │   ├── engine/
│   │   │   ├── cpp/               # Optional C++17 simulation engine
│   │   │   └── bindings.py        # pybind11 interface
│   │   │
│   │   └── cli.py                 # Typer CLI for reproducible runs
│
├── notebooks/
│   ├── 01_data_exploration.ipynb
│   ├── 02_factor_research.ipynb
│   ├── 03_var_es_backtesting.ipynb
│   ├── 04_portfolio_construction.ipynb
│   └── 05_monte_carlo.ipynb
│
├── tests/
│   ├── test_data.py
│   ├── test_factors.py
│   ├── test_var.py
│   ├── test_backtesting.py
│   ├── test_portfolio.py
│   └── test_engine.py
│
├── results/
│   ├── figures/           # Plots, charts, diagnostics
│   ├── tables/            # CSV summaries, risk reports
│   └── logs/              # Backtest logs, stress test outputs
│
└── docs/
    ├── architecture.md
    ├── methodology.md
    ├── api_reference.md
    └── experiments/
        ├── var_experiment.yaml
        ├── stress_scenarios.yaml
        └── factor_config.yaml
