import numpy as np

from server_selection_functions import *
from game_functions import *
from parameters import *

def test_all_users_sure():
    """ Test for all_users_sure """

    params = set_parameters()

    probabilities = np.array([[1,0,0],[0.95,0.05,0]])
    assert all_users_sure(probabilities) == True

    probabilities = np.array([[1,0,0],[0.95,0.05,0],[0.3,0.5,0.2]])
    assert all_users_sure(probabilities) == False

def test_server_selection():
    """ Test for server_selection """

    params = set_parameters()
    params["U"] = 3
    params["S"] = 3

    probabilities = np.array([[1,0,0],[0.95,0.05,0],[0.3,0.5,0.2]])

    # Run multiple times to get result based on probabilities
    tmp = []
    for i in range(100):
        tmp.append(server_selection(probabilities, **params))
    tmp = np.array(tmp)

    # Transpose so that each row contains what the user selected
    tmp = tmp.T
    server_selected = []
    for row in tmp:
        values, counts = np.unique(row, return_counts=True)
        index = np.argmax(counts)
        server_selected.append(values[index])
    server_selected
    assert np.array_equal(server_selected, np.array([0, 0, 1]))

    # return parameters to the original values
    params = set_parameters()

def test_game_converged():
    """ Test for game_converged """

    params = set_parameters()

    # nothing changed
    b = np.array([1,1,0])
    b_old = np.array([1,1,0])
    prices = np.array([0.5,0.8,0.2])
    prices_old = np.array([0.5,0.8,0.2])
    assert game_converged(b,b_old,prices,prices_old, **params) == True

    # b changed
    b = np.array([2,1,0])
    b_old = np.array([1,1,0])
    prices = np.array([0.5,0.8,0.2])
    prices_old = np.array([0.5,0.8,0.2])
    assert game_converged(b,b_old,prices,prices_old, **params) == False

    # prices changed
    b = np.array([1,1,0])
    b_old = np.array([1,1,0])
    prices = np.array([0.6,0.8,0.2])
    prices_old = np.array([0.5,0.8,0.2])
    assert game_converged(b,b_old,prices,prices_old, **params) == False

    # both changed
    b = np.array([1,3,0])
    b_old = np.array([1,1,0])
    prices = np.array([0.6,0.8,0.4])
    prices_old = np.array([0.5,0.8,0.2])
    assert game_converged(b,b_old,prices,prices_old, **params) == False
