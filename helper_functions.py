'''
Helper functions that are used in the simulation
'''

import numpy as np

from runparams import *

def initialize():
    '''
    Initialize the probabilities for the simulation

    Parameters
    ----------

    none

    Returns
    -------

    probabilities: 1-D array
        Each row represents a user and each column the probability that the user
        will select the specific server.
    prices: 1-D array
        Each column represents the price set by the server
    '''

    probabilities = np.ones((U,S))/S
    prices = np.ones(S)*10
    return probabilities, prices
