import numpy as np
from scipy.stats import chi2

# Portion of Failure

def kupiec_pof(
        failures: int,
        observations: int,
        confidence_level: float = 0.99,
        test_confidence: float = 0.95
) -> dict:
    if observations <= 0:
        raise ValueError("observations must be positive")
    if failures < 0 or failures > observations:
        raise ValueError("failures must be between zero and observations")
    if not 0 < confidence_level < 1:
        raise ValueError("confidence_level must be between 0 and 1")
    if not 0 < test_confidence < 1:
        raise ValueError("test_confidence must be between 0 and 1")

    alpha = 1 - confidence_level
    successes = observations - failures

    # Omit zero-count terms from the log likelihood. This keeps the
    # boundary cases (zero or all failures) finite and well-defined.
    expected_log_likelihood = (
        successes * np.log(confidence_level)
        + failures * np.log(alpha)
    )
    failure_rate = failures / observations
    empirical_log_likelihood = 0.0
    if successes:
        empirical_log_likelihood += successes * np.log(1 - failure_rate)
    if failures:
        empirical_log_likelihood += failures * np.log(failure_rate)

    pof = -2 * (expected_log_likelihood - empirical_log_likelihood)
    
    p_value = 1 - chi2.cdf(pof, df=1)
    critical_value = chi2.ppf(test_confidence, df=1)

    is_rejected = pof > critical_value
    
    
    return {
        "lr_pof": float(pof),
        "p_value": float(p_value),
        "is_rejected": bool(is_rejected)
    }


# Time until first failure
def kupiec_tff (
        first_failure_day: int,
        confidence_level: float = 0.99,
        test_confidence: float = 0.95
) -> dict:

    if first_failure_day == 0:
        return {
            "lr_tff": np.nan,
            "p_value": np.nan,
            "is_rejected": False 
        }

    alpha = 1 - confidence_level

    theory = alpha * (confidence_level)**(first_failure_day - 1) 
    reality = (1/first_failure_day) * (1- (1/first_failure_day))**(first_failure_day-1)

    tff = -2* np.log(theory/reality)

    p_value = 1 - chi2.cdf(tff, df=1)
    critical_value = chi2.ppf(test_confidence, df=1)

    is_rejected = tff > critical_value

    return {
        "lr_tff": float(tff),
        "p_value": float(p_value),
        "is_rejected": bool(is_rejected)
    }


# https://www.value-at-risk.net/backtesting-independence-tests/#exercise_14_6
def christoffersen(
        hits: np.ndarray,
        test_confidence: float = 0.95  
) -> dict:
    n00 = np.sum((hits[:-1] == 0) & (hits[1:] == 0))
    n01 = np.sum((hits[:-1] == 0) & (hits[1:] == 1))
    n10 = np.sum((hits[:-1] == 1) & (hits[1:] == 0))
    n11 = np.sum((hits[:-1] == 1) & (hits[1:] == 1))

    if (n01 + n11) == 0:
        print("Test")
        return {
            "lr_ind": np.nan,
            "p_value": np.nan,
            "is_rejected": False
        }

    q0 = n00 / (n00 + n01)
    q1 = n10 / (n10 + n11)
    qn = (n00 + n10) / (n00 + n01 + n10 + n11)
    Lambda = ((1-qn)**(n01 + n11) * (qn)**(n00 + n10)) / ((1-q0)**n01 * q0**n00 * (1-q1)**n11 * q1**n10)

    lr_ind = -2 * np.log(Lambda)
    p_value = 1 - chi2.cdf(lr_ind, df=1)

    critical_value = chi2.ppf(test_confidence, df=1)
    is_rejected = lr_ind > critical_value

    return {
        "lr_ind": float(lr_ind),
        "p_value": float(p_value),
        "is_rejected": bool(is_rejected)
    }
    