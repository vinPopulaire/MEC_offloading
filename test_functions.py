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

def test_update_probabilites():
    """ Test for update_probabilities """

    params = set_parameters()

    # 3 users and 3 servers
    probabilities = np.array([np.array([0.3, 0.3, 0.4]),np.array([0.4, 0.3, 0.3]),np.array([0.3, 0.3, 0.4])])
    b = np.array([2,1,1])
    server_selected = np.array([0, 0, 2])

    bytes_to_server = np.array([3.0, 0.0, 1.0])
    all_bytes_to_server = np.array([np.array([3.0,0.0,1.0])])
    fs = np.array([0.025, 0.026, 0.027])
    all_fs = np.array([fs])
    learning_rate = 0.7

    sum_Rs = 0.025*0.75 + 0.027*0.25
    manual_prob = np.array([np.array([0.3 + 0.7*0.025*0.75/sum_Rs*0.7, 0.3 - 0.7*0.025*0.75/sum_Rs*0.3, 0.4 - 0.7*0.025*0.75/sum_Rs*0.4]), np.array([0.4 + 0.7*0.025*0.75/sum_Rs*0.6, 0.3 - 0.7*0.025*0.75/sum_Rs*0.3, 0.3 - 0.7*0.025*0.75/sum_Rs*0.3]), np.array([0.3 - 0.7*0.027*0.25/sum_Rs*0.3, 0.3 - 0.7*0.027*0.25/sum_Rs*0.3, 0.4 + 0.7*0.027*0.25/sum_Rs*0.6]) ])
    automatic_prob = update_probabilities(probabilities, server_selected, b, all_bytes_to_server, all_fs, **params)

    assert np.allclose(manual_prob, automatic_prob)

def test_play_offloading_game():
    """ Test for play_offloading_game """

    params = set_parameters()
    U = params["U"] = 3
    S = params["S"] = 3
    a = params["a"] = np.array([20, 30, 40])
    l = params["l"] = 1000
    k = params["k"] = 100

    # 3 users and 3 servers
    server_selected = np.array([0, 0, 2])
    b_old = np.ones(U)
    prices = np.ones(S)

    manual_b = np.array([(2/l)*(k*l/a[0] - 1), (2/l)*(k*l/a[1] - 1), (2/l)*(k*l/a[2] - 1)])

    automatic_b = play_offloading_game(server_selected, b_old, prices, **params)
    assert np.allclose(manual_b, automatic_b)

    params = set_parameters()

def test_play_pricing_game():
    """ Test for play_pricing_game """

    params = set_parameters()
    U = params["U"] = 3
    S = params["S"] = 3
    a = params["a"] = np.array([20, 30, 40])
    l = params["l"] = 1000
    k = params["k"] = 100
    c = params["c"] = np.array([0.2, 0.3, 0.4])
    fs = params["fs"] = np.array([0.025, 0.026, 0.027])
    price_min = params["price_min"]

    server_selected = np.array([0, 0, 2])
    b = np.array([2,1,1])

    manual_price = np.array([
        np.sqrt((k*l*c[0]*(b[1]/a[0] + b[0]/a[1]) / ((1-fs[0])* (b[0] + b[1])))),
        np.sqrt((k*l*c[1]*( 0 / ((1-fs[1])* 0.1 )))),
        np.sqrt((k*l*c[2]*( 0 / ((1-fs[1])* 0.1 ))))
            ])

    manual_price[manual_price<price_min] = price_min

    automatic_price = play_pricing_game(server_selected, b, **params)

    assert np.allclose(manual_price, automatic_price)

    params = set_parameters()
