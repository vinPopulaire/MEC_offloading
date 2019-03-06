'''
Plot functions to graphically present simulation results
'''

import numpy as np
import matplotlib.pyplot as plt

from parameters import SAVE_FIGS, ONE_FIGURE

server_names = ['server 1', 'server 2', 'server 3',
                'server 4', 'server 5']

color_sequence = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c']

def setup_plots(suptitle):
    '''
    Basic setup of plots so it can be reused on plot functions

    Parameters
    ----------

    suptitle: string
        Description of the plot that will appear on the top

    Returns
    -------
    Figure and axis matplotlib structs

    '''
    fig, ax = plt.subplots(1, 1, figsize=(12, 9))
    fig.suptitle(suptitle)

    ax.spines['top'].set_visible(False)
    ax.spines['right'].set_visible(False)

    # Provide tick lines across the plot to help viewers trace along
    # the axis ticks.
    plt.grid(True, 'major', 'y', ls='--', lw=.5, c='k', alpha=.3)

    # Remove the tick marks; they are unnecessary with the tick lines we just
    # plotted.
    plt.tick_params(axis='both', which='both', bottom=True, top=False,
                    labelbottom=True, left=False, right=False, labelleft=True)

    return fig, ax

def create_plot_server(result, path_name, suptitle, xlabel, ylabel, offset):
    '''
    Generate the plot needed

    Parameters
    ----------

    result: 2-d array
        Each row is a different timeslot

    Returns
    -------
    Plot

    '''
    if ONE_FIGURE == False:
        fig, ax = setup_plots(suptitle)

    y_positions = []

    for index, row in enumerate(result):

        line = plt.plot(row, lw=2.5, color=color_sequence[index])

        # set the text to start on the y of the last value of the line
        y_pos = row[-1]
        server_name = server_names[index]
        # move based on offset if names overlap on plot
        while y_pos in y_positions:
            y_pos += offset

        y_positions.append(y_pos)

        plt.text(len(row) + 5, y_pos, server_name, fontsize=14, color=color_sequence[index])

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)

    if SAVE_FIGS == True and ONE_FIGURE == False:
        plt.savefig("plots/" + path_name + ".png")
    else:
        plt.show(block=False)


def plot_data_offloading_of_users(all_bytes_offloaded):
    '''
    Plot the data each user is offloading in each timeslot

    Parameters
    ----------

    all_bytes_offloaded: 2-d array
        Contains on each row the amount of data each user is offloading. Each row is
        a different timeslot

    Returns
    -------
    Plot

    '''
    result = all_bytes_offloaded

    # Each row on the transposed matrix contains the data the user offloads
    # in each timeslot. Different rows mean different user.
    result = np.transpose(result)

    suptitle = "Data each user is offloading in each timeslot"

    if ONE_FIGURE == False:
        fig, ax = setup_plots(suptitle)

    for index, row in enumerate(result):

        line = plt.plot(row, lw=2.5)

    plt.xlabel('iterations')
    plt.ylabel('amount of data (bytes)')

    path_name = "all_bytes_offloaded"
    if SAVE_FIGS == True and ONE_FIGURE == False:
        plt.savefig("plots/" + path_name + ".png")
    else:
        plt.show(block=False)


def plot_user_utility(all_user_utility):
    '''
    Plot the utility each user has in each timeslot

    Parameters
    ----------

    all_user_utility: 2-d array
        Contains on each row the utility value each user has. Each row is
        a different timeslot

    Returns
    -------
    Plot

    '''
    result = all_user_utility

    # Each row on the transposed matrix contains the data the user offloads
    # in each timeslot. Different rows mean different user.
    result = np.transpose(result)

    suptitle = "Utility each user has in each timeslot"

    if ONE_FIGURE == False:
        fig, ax = setup_plots(suptitle)

    for index, row in enumerate(result):

        line = plt.plot(row, lw=2.5)

    plt.xlabel('iterations')
    plt.ylabel('utility')

    path_name = "all_user_utility"
    if SAVE_FIGS == True and ONE_FIGURE == False:
        plt.savefig("plots/" + path_name + ".png")
    else:
        plt.show(block=False)


def plot_num_of_users_on_each_server(all_server_selected, S, **params):
    '''
    Plot number of users on each server every timeslot

    Parameters
    ----------

    all_server_selected: 2-d array
        Contains on each row the server each user has selected. Each row is
        a different timeslot
    S: int
        Number of servers

    Returns
    -------
    Plot

    '''
    # How many users each server has each timeslot
    result = np.empty((0, S), int)
    for row in all_server_selected:
        # the bincount finds how many times each server has been selected
        result = np.append(result, [np.bincount(row, minlength=S)], axis=0)

    # Each row on the transposed matrix contains how many users the server has
    # in each timeslot. Different rows mean different servers.
    result = np.transpose(result)

    offset = np.abs(np.max(result) - np.min(result))*0.03
    if offset < 0.005:
        offset = 0.005 + np.abs(np.max(result))*0.005;

    path_name = "all_server_selected"
    suptitle = "Number of users each server has in each timeslot"
    xlabel = "timeslots"
    ylabel = "num of users"

    create_plot_server(result, path_name, suptitle, xlabel, ylabel, offset)


def plot_pricing_of_each_server(all_prices):
    '''
    Plot pricing of each server on every timeslot

    Parameters
    ----------

    all_prices: 2-d array
        Contains on each row the price each server has chosen. Each row is
        a different timeslot

    Returns
    -------
    Plot

    '''
    result = all_prices

    # Each row on the transposed matrix contains the price the server has
    # in each timeslot. Different rows mean different servers.
    result = np.transpose(result)

    offset = np.abs(np.max(result) - np.min(result))*0.03
    if offset < 0.005:
        offset = 0.005 + np.abs(np.max(result))*0.005;

    path_name = "all_prices"
    suptitle = "Price each server has selected in each timeslot"
    xlabel = "timeslots"
    ylabel = "price"

    create_plot_server(result, path_name, suptitle, xlabel, ylabel, offset)


def plot_receiving_data_on_each_server(all_bytes_to_server):
    '''
    Plot the data each server is receiving in each timeslot

    Parameters
    ----------

    all_bytes_to_server: 2-d array
        Contains on each row the amount of data each server is receiving. Each row is
        a different timeslot

    Returns
    -------
    Plot

    '''
    result = all_bytes_to_server

    # Each row on the transposed matrix contains the data the server receives
    # in each timeslot. Different rows mean different servers.
    result = np.transpose(result)

    offset = np.abs(np.max(result) - np.min(result))*0.03
    if offset < 0.005:
        offset = 0.005 + np.abs(np.max(result))*0.005;

    path_name = "all_bytes_to_server"
    suptitle = "Data each server is receiving in each timeslot"
    xlabel = "timeslots"
    ylabel = "amount of data (bytes)"

    create_plot_server(result, path_name, suptitle, xlabel, ylabel, offset)


def plot_server_welfare(all_server_welfare):
    '''
    Plot the welfare of each server in each timeslot

    Parameters
    ----------

    all_server_welfare: 2-d array
        Contains on each row the welfare of each server. Each row is
        a different timeslot

    Returns
    -------
    Plot

    '''
    result = all_server_welfare

    # Each row on the transposed matrix contains the data the user offloads
    # in each timeslot. Different rows mean different user.
    result = np.transpose(result)

    offset = np.abs(np.max(result) - np.min(result))*0.03
    if offset < 0.005:
        offset = 0.005 + np.abs(np.max(result))*0.005;

    path_name = "all_server_welfare"
    suptitle = "Welfare of the server at the end of each timeslot"
    xlabel = "timeslots"
    ylabel = "welfare"

    create_plot_server(result, path_name, suptitle, xlabel, ylabel, offset)


def plot_server_Rs(all_Rs):
    '''
    Plot the competitiveness score each server has in each timeslot

    Parameters
    ----------

    all_Rs: 2-d array
        Contains on each row the Rs of each server. Each row is
        a different timeslot

    Returns
    -------
    Plot

    '''
    result = all_Rs

    # Each row on the transposed matrix contains the data the user offloads
    # in each timeslot. Different rows mean different user.
    result = np.transpose(result)

    offset = np.abs(np.max(result) - np.min(result))*0.03
    if offset < 0.005:
        offset = 0.005 + np.abs(np.max(result))*0.005;

    path_name = "all_Rs"
    suptitle = "Rs of the server at the end of each timeslot"
    xlabel = "timeslots"
    ylabel = "Rs"

    create_plot_server(result, path_name, suptitle, xlabel, ylabel, offset)


def plot_server_congestion(all_congestion):
    '''
    Plot the peak to average ratio each server has in each timeslot

    Parameters
    ----------

    all_congestion: 2-d array
        Contains on each row the congestion of each server. Each row is
        a different timeslot

    Returns
    -------
    Plot

    '''
    result = all_congestion

    # Each row on the transposed matrix contains the data the user offloads
    # in each timeslot. Different rows mean different user.
    result = np.transpose(result)

    offset = np.abs(np.max(result) - np.min(result))*0.03
    if offset < 0.005:
        offset = 0.005 + np.abs(np.max(result))*0.005;

    path_name = "all_congestion"
    suptitle = "congestion of the server at the end of each timeslot"
    xlabel = "timeslots"
    ylabel = "congestion"

    create_plot_server(result, path_name, suptitle, xlabel, ylabel, offset)


def plot_server_penetration(all_penetration):
    '''
    Plot the penetration score each server has in each timeslot

    Parameters
    ----------

    all_penetration: 2-d array
        Contains on each row the penetration score of each server. Each row is
        a different timeslot

    Returns
    -------
    Plot

    '''
    result = all_penetration

    # Each row on the transposed matrix contains the data the user offloads
    # in each timeslot. Different rows mean different user.
    result = np.transpose(result)

    offset = np.abs(np.max(result) - np.min(result))*0.03
    if offset < 0.005:
        offset = 0.005 + np.abs(np.max(result))*0.005;

    path_name = "all_penetration"
    suptitle = "penetration of the server at the end of each timeslot"
    xlabel = "timeslots"
    ylabel = "penetration"

    create_plot_server(result, path_name, suptitle, xlabel, ylabel, offset)


def plot_server_discount(all_fs):
    '''
    Plot the discount each server has in each timeslot

    Parameters
    ----------

    all_fs: 2-d array
        Contains on each row the discount of each server. Each row is
        a different timeslot

    Returns
    -------
    Plot

    '''
    result = all_fs

    # Each row on the transposed matrix contains the data the user offloads
    # in each timeslot. Different rows mean different user.
    result = np.transpose(result)

    offset = np.abs(np.max(result) - np.min(result))*0.03
    if offset < 0.005:
        offset = 0.005 + np.abs(np.max(result))*0.005;

    path_name = "all_fs"
    suptitle = "discount of the server at the end of each timeslot"
    xlabel = "timeslots"
    ylabel = "discount"

    create_plot_server(result, path_name, suptitle, xlabel, ylabel, offset)


def plot_server_relative_price(all_relative_price):
    '''
    Plot the relative price each server sets in each timeslot

    Parameters
    ----------

    all_relative_price: 2-d array
        Contains on each row the relative_price of each server. Each row is
        a different timeslot

    Returns
    -------
    Plot

    '''
    result = all_relative_price

    # Each row on the transposed matrix contains the data the user offloads
    # in each timeslot. Different rows mean different user.
    result = np.transpose(result)

    offset = np.abs(np.max(result) - np.min(result))*0.03
    if offset < 0.005:
        offset = 0.005 + np.abs(np.max(result))*0.005;

    path_name = "all_relative_price"
    suptitle = "Relative pricing of the server at the end of each timeslot"
    xlabel = "timeslots"
    ylabel = "relative pricing"

    create_plot_server(result, path_name, suptitle, xlabel, ylabel, offset)


def plot_server_cost(all_c):
    '''
    Plot the cost each server has in each timeslot

    Parameters
    ----------

    all_c: 2-d array
        Contains on each row the server computing cost of each server. Each row is
        a different timeslot

    Returns
    -------
    Plot

    '''
    result = all_c

    # Each row on the transposed matrix contains the data the user offloads
    # in each timeslot. Different rows mean different user.
    result = np.transpose(result)

    offset = np.abs(np.max(result) - np.min(result))*0.03
    if offset < 0.005:
        offset = 0.005 + np.abs(np.max(result))*0.005;

    path_name = "all_c"
    suptitle = "computing cost of the server at the end of each timeslot"
    xlabel = "timeslots"
    ylabel = "computing cost"

    create_plot_server(result, path_name, suptitle, xlabel, ylabel, offset)


def plot_user_probability_to_select_server(user_id, all_probabilities):
    '''
    Plot the probability that the user will select each server in each timeslot

    Parameters
    ----------

    all_probabilities: 3-d array
        The first dimension contains the different users,
        The second dimension contains the timeslots,
        The third dimension contains the probabilities that the user selects the servers
        a different timeslot

    Returns
    -------
    Plot

    '''
    result = all_probabilities[user_id]

    # Each row on the transposed matrix contains the data the user offloads
    # in each timeslot. Different rows mean different user.
    result = np.transpose(result)

    offset = np.abs(np.max(result) - np.min(result))*0.03
    if offset < 0.005:
        offset = 0.005 + np.abs(np.max(result))*0.005;

    path_name = "all_probabilities_user_" + str(user_id)
    suptitle = "Probability that the user " + str(user_id) + " will select each server at the end of each timeslot"
    xlabel = "timeslots"
    ylabel = "probabilities"

    create_plot_server(result, path_name, suptitle, xlabel, ylabel, offset)

