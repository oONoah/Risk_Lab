import numpy as np
from scipy.stats import chi2

# Portion of Failure

def kupiec_pof(
        failures: int,
        observations: int,
        confidence_level: float = 0.99
) -> dict:
    
    alpha = 1 - confidence_level
    successes = observations - failures

    theory = confidence_level ** successes * alpha ** failures
    realtiy = (1 - (failures/observations))**successes * (failures/observations)**failures

    pof = -2*np.log(theory/realtiy)
    
    p_value = 1 - chi2.cdf(pof, df=1)
    critical_value = chi2.ppf(confidence_level, df=1)

    is_rejected = pof > critical_value
    
    
    return {
        "lr_pof": float(pof),
        "p_value": float(p_value),
        "is_rejected": bool(is_rejected)
    }


# Time until first failure
def kupiec_tff (
        first_failure_day: int,
        confidance_level: float = 0.99
) -> dict:


    alpha = 1 - confidance_level

    theory = alpha * (confidance_level)**(first_failure_day - 1) 
    reality = (1/first_failure_day) * (1- (1/first_failure_day))**(first_failure_day-1)

    tff = -2* np.log(theory/reality)

    p_value = 1 - chi2.cdf(tff, df=1)
    critical_value = chi2.ppf(confidance_level, df=1)

    is_rejected = tff > critical_value

    return {
        "lr_tff": float(tff),
        "p_value": float(p_value),
        "is_rejected": bool(is_rejected)
    }