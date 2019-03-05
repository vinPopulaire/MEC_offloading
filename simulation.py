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
from create_plots import *

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

results = {}
for case in cases:

    if LOAD_SAVED_PARAMETERS == True:
        print("Loading parameters")
        infile = "saved_runs/parameters/" + case["users"] + "_" + case["servers"] + "_lr_" + "0.10"

        with open(infile, 'rb') as in_strm:
            params = dill.load(in_strm)
    else:
        # Set random parameter in order to generate the same parameters
        print("Generating new parameters")
        np.random.seed(42)
        params = set_parameters(case)

    U = params['U']
    S = params['S']
    fs = params['fs']
    c = params['c']

    start = time.time()

    # Initialize empty arrays for results
    all_server_selected = all_bytes_offloaded = all_user_utility = np.empty((0,U), int)
    all_bytes_to_server = all_prices = all_c = all_fs = all_relative_price = all_server_welfare = all_Rs = all_congestion = all_penetration = np.empty((0,S), int)
    all_probabilities = [[] for i in range(U)]

    # Get the initial values for probabilities and prices
    probabilities, prices = initialize(**params)

    for i in range(U):
        all_probabilities[i].append(probabilities[i])

    if CONSTANT_PRICING:
        # Set constant price if needed
        constant_price = np.array([1.96, 1.88, 1.94, 1.78, 1.92])
        prices = constant_price
        all_prices = np.append(all_prices, [prices], axis=0)

    # Repeat until every user is sure on the selected server
    while not all_users_sure(probabilities):
        # Each user selects a server to which he will offload computation
        server_selected = server_selection(probabilities, **params)
        # Add the selected servers as a row in the matrix
        all_server_selected = np.append(all_server_selected, [server_selected], axis=0)

        # Game starts in order to converge to the optimum values of data offloading
        # Repeat until convergence for both users and servers
        b_old = np.ones(U)
        prices_old = np.ones(S)

        converged = False
        while not converged:
            # Users play a game to converge to the Nash Equilibrium
            b = play_offloading_game(server_selected, b_old, prices_old, **params)

            if CONSTANT_PRICING:
                # Servers set their next price as they had initally set
                prices = constant_price
            else:
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

        # Calculate the welfare of the servers
        server_welfare = calculate_server_welfare(prices, bytes_to_server, **params)
        all_server_welfare = np.append(all_server_welfare, [server_welfare], axis=0)

        # Calculate the perceived utility of the users
        user_utility = calculate_user_utility(b, server_selected, prices, **params)
        all_user_utility = np.append(all_user_utility, [user_utility], axis=0)

        # Calculate the competitiveness of each server
        Rs,relative_price,congestion,penetration = calculate_competitiveness(all_bytes_to_server, all_fs, all_prices, **params)

        all_Rs = np.append(all_Rs, [Rs], axis=0)
        all_congestion = np.append(all_congestion, [congestion], axis=0)
        all_penetration = np.append(all_penetration, [penetration], axis=0)
        all_relative_price = np.append(all_relative_price, [relative_price], axis=0)

        # Update the probabilities
        probabilities = update_probabilities(Rs, probabilities, server_selected, b, **params)

        for i in range(U):
            all_probabilities[i].append(probabilities[i])

    for i in range(len(all_probabilities)):
        all_probabilities[i] = np.array(all_probabilities[i])
    all_probabilities = np.array(all_probabilities)

    # Keep results in a dictionary in order to save and plot them
    key = case["users"] + "_" + case["servers"]
    results[key] = {
        "all_bytes_offloaded": all_bytes_offloaded,
        "all_server_selected": all_server_selected,
        "all_prices": all_prices,
        "all_bytes_to_server": all_bytes_to_server,
        "all_server_welfare": all_server_welfare,
        "all_user_utility": all_user_utility,
        "all_Rs": all_Rs,
        "all_relative_price": all_relative_price,
        "all_congestion": all_congestion,
        "all_penetration": all_penetration,
        "all_fs": all_fs,
        "all_c": all_c,
        "all_probabilities": all_probabilities
        }

    end = time.time()
    print("Time of simulation:")
    print(end - start)

    # Save parameters and results
    if SAVE_PARAMETERS == True:
        outfile = "saved_runs/parameters/" + case["users"] + "_" + case["servers"] + "_lr_" + "{0:.2f}".format(params["learning_rate"])

        with open(outfile, 'wb') as fp:
            dill.dump(params, fp)

    if SAVE_RESULTS == True:
        outfile = 'saved_runs/results/' + case["users"] + "_" + case["servers"] + "_lr_" + "{0:.2f}".format(params["learning_rate"]) + "_constant-pricing"

        with open(outfile , 'wb') as fp:
            dill.dump(results[key], fp)

# Create the plots
create_plots(results, cases, params)
