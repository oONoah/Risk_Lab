import numpy as np


def price_knockout_option_mc(
    s0: float,
    barrier: float,
    payoff_amount: float,
    mu: float,
    sigma: float,
    t_years: float = 1,
    steps: int = 252,
    num_simulations: int = 10000,
) -> float:
    if s0 < barrier:
        return 0.0

    dt = t_years / steps

    Z = np.random.standard_normal((num_simulations, steps))

    drift = (mu - sigma**2 / 2) * dt
    diffusion = sigma * np.sqrt(dt) * Z

    log_returns = np.cumsum(drift + diffusion, axis=1)
    paths = s0 * np.exp(log_returns)

    min_prices = np.min(paths, axis=1)
    survived = min_prices >= barrier
    print(min_prices)
    print(survived)
    



    return float(np.mean(survived * payoff_amount))


