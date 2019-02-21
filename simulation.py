# -*- coding: utf-8 -*-
"""
    MEC_offloading.simulation
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Simulation for the MEC_offloading

    :copyright: (c) 2018 by Giorgos Mitsis.
    :license: MIT License, see LICENSE for more details.
"""

import numpy as np
import matplotlib.pyplot as plt

from parameters import *
from helper_functions import *
from game_functions import *
from server_selection_functions import *
from metrics import *
from plots import *

import time
import itertools
import dill

# Keep only three decimal places when printing numbers
np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

# Generate all cases
cases_setup = {
        'users': ['homo','hetero'],
        'servers': ['homo','hetero','one-dominant','two-dominant']
        }

keys, values = zip(*cases_setup.items())

# Select which case to run
# cases = [{"users": "hetero", "servers": "two-dominant"}]
cases = [dict(zip(keys, v)) for v in itertools.product(*values)]

for case in cases:

    if LOAD_SAVED_PARAMETERS == True:
        print("Loading parameters")
        infile = "saved_runs/saved_parameters_" + case["users"] + "_" + case["servers"]
        with open(infile, 'rb') as in_strm:
            params = dill.load(in_strm)
    else:
        # set random parameter in order to generate the same parameters
        print("Generating new parameters")
        np.random.seed(42)
        params = set_parameters(case)

    U = params['U']
    S = params['S']
    fs = params['fs']
    c = params['c']

    start = time.time()

    all_server_selected = np.empty((0,U), int)
    all_bytes_offloaded = np.empty((0,U), int)
    all_bytes_to_server = np.empty((0,S), int)
    all_prices = np.empty((0,S), int)
    all_c = np.empty((0,S), int)
    all_fs = np.empty((0,S), int)
    all_relative_price = np.empty((0,S), int)
    all_server_welfare = np.empty((0,S), int)

    all_Rs = np.empty((0,S), int)
    all_congestion = np.empty((0,S), int)
    all_penetration = np.empty((0,S), int)

    all_probabilities = [[] for i in range(U)]

    # np.random.seed(2)

    # Get the initial values for probabilities and prices
    probabilities, prices = initialize(**params)

    for i in range(U):
        all_probabilities[i].append(probabilities[i])

    all_prices = np.append(all_prices, [prices], axis=0)

    # Repeat until every user is sure on the selected server
    while not all_users_sure(probabilities):
        # Each user selects a server to which he will offload computation
        server_selected = server_selection(probabilities, **params)
        # add the selected servers as a row in the matrix
        all_server_selected = np.append(all_server_selected, [server_selected], axis=0)

        # Game starts in order to converge to the optimum values of data offloading
        # Repeat until convergence for both users and servers
        b_old = np.ones(U)
        prices_old = np.ones(S)

        converged = False
        while not converged:
            # Users play a game to converge to the Nash Equilibrium
            b = play_offloading_game(server_selected, b_old, prices_old, **params)

            # Servers update their prices based on the users' offloading of data
            prices = play_pricing_game(server_selected, b, **params)

            # Check if game has converged
            converged = game_converged(b,b_old,prices,prices_old, **params)

            b_old = b
            prices_old = prices

        all_bytes_offloaded = np.append(all_bytes_offloaded, [b], axis=0)

        # Find all bytes that are offloaded to each server
        bytes_to_server = np.bincount(server_selected, b, minlength=S)
        all_bytes_to_server = np.append(all_bytes_to_server, [bytes_to_server], axis=0)

        all_prices = np.append(all_prices, [prices], axis=0)

        all_fs = np.append(all_fs, [fs], axis=0)
        all_c = np.append(all_c, [c], axis=0)

        server_welfare = calculate_server_welfare(prices, bytes_to_server, **params)
        all_server_welfare = np.append(all_server_welfare, [server_welfare], axis=0)

        Rs,relative_price,congestion,penetration = calculate_competitiveness(all_bytes_to_server, all_fs, all_prices, **params)
        all_Rs = np.append(all_Rs, [Rs], axis=0)
        all_congestion = np.append(all_congestion, [congestion], axis=0)
        all_penetration = np.append(all_penetration, [penetration], axis=0)
        all_relative_price = np.append(all_relative_price, [relative_price], axis=0)
        probabilities = update_probabilities(Rs, probabilities, server_selected, b, **params)

        for i in range(U):
            all_probabilities[i].append(probabilities[i])

    for i in range(len(all_probabilities)):
        all_probabilities[i] = np.array(all_probabilities[i])
    all_probabilities = np.array(all_probabilities)

    end = time.time()
    print("Time of simulation:")
    print(end - start)

    if ONE_FIGURE == True:
        plt.figure(figsize=(40.0, 30.0))
        plt.subplot(4,4,1)
        plot_data_offloading_of_users(all_bytes_offloaded)
        plt.subplot(4,4,2)
        plot_num_of_users_on_each_server(all_server_selected, **params)
        plt.subplot(4,4,3)
        plot_pricing_of_each_server(all_prices)
        plt.subplot(4,4,4)
        plot_receiving_data_on_each_server(all_bytes_to_server)
        plt.subplot(4,4,5)
        plot_server_welfare(all_server_welfare)
        plt.subplot(4,4,6)
        plot_server_Rs(all_Rs)
        plt.subplot(4,4,7)
        plot_server_congestion(all_congestion)
        plt.subplot(4,4,8)
        plot_server_penetration(all_penetration)
        plt.subplot(4,4,9)
        plot_server_discount(all_fs)
        plt.subplot(4,4,10)
        plot_server_cost(all_c)
        plt.subplot(4,4,11)
        plot_server_relative_price(all_relative_price)
    else:
        plot_data_offloading_of_users(all_bytes_offloaded)
        plot_num_of_users_on_each_server(all_server_selected, **params)
        plot_pricing_of_each_server(all_prices)
        plot_receiving_data_on_each_server(all_bytes_to_server)
        plot_server_welfare(all_server_welfare)
        plot_server_Rs(all_Rs)
        plot_server_congestion(all_congestion)
        plot_server_penetration(all_penetration)
        plot_server_discount(all_fs)
        plot_server_cost(all_c)
        plot_server_relative_price(all_relative_price)

    # for user in range(U):
    #     plot_user_probability_to_select_server(user, all_probabilities)

    # Go to parameters.py to change the setting
    if SAVE_FIGS == False:
        plt.show()
    if SAVE_FIGS == True and ONE_FIGURE == True:
        plt.savefig("plots/" + case["users"] + "_" + case["servers"] + ".png")

    # save parameters and results
    if SAVE_PARAMETERS == True:
        outfile = "saved_runs/saved_parameters_" + case["users"] + "_" + case["servers"]
        with open(outfile, 'wb') as fp:
            dill.dump(params, fp)

    results = {
        "all_bytes_offloaded": all_bytes_offloaded,
        "all_server_selected": all_server_selected,
        "all_prices": all_prices,
        "all_bytes_to_server": all_bytes_to_server,
        "all_server_welfare": all_server_welfare,
        "all_Rs": all_Rs,
        "all_penetration": all_penetration,
        "all_fs": all_fs,
        "all_c": all_c,
        "all_relative_price": all_relative_price,
        "all_probabilities": all_probabilities
        }

    outfile = 'saved_runs/results_' + case["users"] + "_" + case["servers"]
    with open(outfile , 'wb') as fp:
        dill.dump(results, fp)
