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
from plots import *

import time

# keep only three decimal places when printing numbers
np.set_printoptions(formatter={'float': lambda x: "{0:0.3f}".format(x)})

start = time.time()

all_server_selected = np.empty((0,U), int)
all_bytes_offloaded = np.empty((0,U), int)
all_bytes_to_server = np.empty((0,S), int)
all_prices = np.empty((0,S), int)
all_fs = np.empty((0,S), int)

np.random.seed(2)

# Get the initial values for probabilities and prices
probabilities, prices = initialize()

all_prices = np.append(all_prices, [prices], axis=0)

# Repeat until every user is sure on the selected server
while not all_users_sure(probabilities):
    # Each user selects a server to which he will offload computation
    server_selected = server_selection(probabilities)
    # add the selected servers as a row in the matrix
    all_server_selected = np.append(all_server_selected, [server_selected], axis=0)

    # Game starts in order to converge to the optimum values of data offloading
    # Repeat until convergence for both users and servers
    b_old = np.ones(U)
    prices_old = np.ones(S)

    converged = False
    while not converged:
        # Users play a game to converge to the Nash Equilibrium
        b = play_offloading_game(server_selected, b_old, prices_old)

        # Servers update their prices based on the users' offloading of data
        prices = play_pricing_game(server_selected, b)

        # Check if game has converged
        converged = game_converged(b,b_old,prices,prices_old)

        b_old = b
        prices_old = prices

    all_bytes_offloaded = np.append(all_bytes_offloaded, [b], axis=0)

    # Find all bytes that are offloaded to each server
    bytes_to_server = np.bincount(server_selected, b, minlength=S)
    all_bytes_to_server = np.append(all_bytes_to_server, [bytes_to_server], axis=0)

    all_prices = np.append(all_prices, [prices], axis=0)

    all_fs = np.append(all_fs, [fs], axis=0)

    probabilities = update_probabilities(probabilities, server_selected, b, all_bytes_to_server, all_fs)

end = time.time()
print("Time of simulation:")
print(end - start)

plot_num_of_users_on_each_server(all_server_selected)
plt.show()
