'''
Parameters of the simulation
'''

import numpy as np

SAVE_FIGS = False
ONE_FIGURE = True
LOAD_SAVED_PARAMETERS = True
SAVE_PARAMETERS = False
SAVE_RESULTS = True

CONSTANT_PRICING = False

def set_parameters(case):
    '''
    Sets the parameters used in the simulation

    Parameters
    ----------

    case: dictionary
        Dictionary containing infromation about whether the user and the servers
        are homogeneous or heterogeneous

    Returns
    ----------

    S: int
        Number of servers
    U: int
        Number of users
    e1: float
        Error for user offloading convergence
    e2: float
        Error for server pricing convergence
    k: int
        parameter of the user's satisfaction function
    l: int
        parameter of the user's satisfaction function
    a: 1-D array
        parameter that reflects users' dynamic behavior to spen more money
        in order to buy computing support from the MEC servers
    b_min: int
        Minimum number of bits that the user is willing to offload
        Same for all users
    b_max: int
        Maximum number of bits that the user is willing to offload
        Same for all users
    c: 1-D array
        parameter that shows the server's computing cost
    fs: 1-D array
        parameter that shows the server's discount
    price_min: int
        Minimum vlaue that the server can set his price
    learning_rate: float
        parameter indicating the learning rate of the server selection learning
        mechanism
    '''

    S = 5
    U = 100
    e1 = 1e-02
    e2 = 1e-02

    k = 100
    l = 1000

    # User parameters
    if case["users"] == "homo":
        a = 1*1e3 * np.ones(U) + 0.5e4
        # a = 1*1e2 * np.ones(U) + 0.5e3
    if case["users"] == "hetero":
        a = 1e3 + np.random.random(U)*1e4

    b_min = 0
    b_max = 1000

    # Server parameters
    if case["servers"] == "homo":
        c = 0.2 * np.ones(S)
        fs = 0.025 * np.ones(S)
    if case["servers"] == "hetero":
        c = np.array([0.12, 0.14, 0.2, 0.17, 0.13])
        fs = np.array([0.05, 0.04, 0.02, 0.03, 0.05])
        # c = 0.2 + np.random.random(S)
        # fs = 0.025 + np.random.random(S) * 0.1
    if case["servers"] == "one-dominant":
        c = np.array([0.1, 0.5, 0.5, 0.5, 0.5])
        fs = np.array([0.1, 0.01, 0.01, 0.01, 0.01])
    if case["servers"] == "two-dominant":
        c = np.array([0.1, 0.1, 0.5, 0.5, 0.5])
        fs = np.array([0.1, 0.1, 0.01, 0.01, 0.01])
        # c = np.array([0.1, 0.12, 0.5, 0.5, 0.5])
        # fs = np.array([0.1, 0.09, 0.01, 0.01, 0.01])

    price_min = 0.5

    learning_rate = 0.2

    return locals()
