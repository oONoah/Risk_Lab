import numpy as np
import scipy as sp

# Portion of Failure

def kupiec_pof_test(
        failures: int,
        observations: int,
        confidence_level: float = 0.99
) -> dict:
    
    alpha = 1 - confidence_level
    successes = observations - failures

    theory = confidence_level ** successes * alpha ** failures
    realtiy = (1 - (failures/observations))**successes * (failures/observations)**failures

    pof = -2*np.log(theory/realtiy)
kupiec_pof_test(5,250)
