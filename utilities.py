"""
Utility function recalled in the 'creator.py' script that checks if the sum of the optimal weights is up to 1

@author: Enrico Pasquariello
@mail: enrico.pasquariello94@gmail.com 
"""

import numpy as np

def check_sum_to_one(w):
    
    return np.sum(w)-1
