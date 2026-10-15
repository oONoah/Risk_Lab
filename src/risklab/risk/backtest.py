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

print(kupiec_pof_test(5,250))
