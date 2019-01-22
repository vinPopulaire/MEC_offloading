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

# keep only three decimal places when printing numbers
np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

params = set_parameters()
U = params['U']
S = params['S']
fs = params['fs']

start = time.time()

all_server_selected = np.empty((0,U), int)
all_bytes_offloaded = np.empty((0,U), int)
all_bytes_to_server = np.empty((0,S), int)
all_prices = np.empty((0,S), int)
all_fs = np.empty((0,S), int)
all_total_discount = np.empty((0,S), int)
all_server_welfare = np.empty((0,S), int)

all_Rs = np.empty((0,S), int)
all_PAR = np.empty((0,S), int)
all_penetration = np.empty((0,S), int)

# np.random.seed(2)

# Get the initial values for probabilities and prices
probabilities, prices = initialize(**params)

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

    server_welfare = calculate_server_welfare(prices, bytes_to_server, **params)
    all_server_welfare = np.append(all_server_welfare, [server_welfare], axis=0)

    Rs,total_discount,PAR,penetration = calculate_competitiveness(all_bytes_to_server, all_fs)
    all_Rs = np.append(all_Rs, [Rs], axis=0)
    all_PAR = np.append(all_PAR, [PAR], axis=0)
    all_penetration = np.append(all_penetration, [penetration], axis=0)
    all_total_discount = np.append(all_total_discount, [total_discount], axis=0)
    probabilities = update_probabilities(Rs, probabilities, server_selected, b, **params)

end = time.time()
print("Time of simulation:")
print(end - start)

plot_data_offloading_of_users(all_bytes_offloaded)
plot_num_of_users_on_each_server(all_server_selected, **params)
plot_pricing_of_each_server(all_prices)
plot_receiving_data_on_each_server(all_bytes_to_server)
plot_server_welfare(all_server_welfare)
plot_server_Rs(all_Rs)
plot_server_PAR(all_PAR)
plot_server_penetration(all_penetration)
plot_server_discount(all_fs)
plot_server_total_discount(all_total_discount)
plt.show()
