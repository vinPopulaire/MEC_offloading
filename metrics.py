'''
Functions to calculate metrics
'''

import numpy as np

def calculate_server_welfare(prices, bytes_to_server, c, fs, **params):
    '''
    Calculates the welfare of each server at the end of the timeslot

    Parameters
    ----------

    prices: 1-D array
        Set the new prices of the servers
    bytes_to_server: 1-D array
        The number of bytes the users have offloaded to the specific server
    c: 1-D array
        parameter that shows the server's computing cost
    fs: 1-D array
        parameter that shows the server's discount

    Returns
    -------

    welfare: 1-D array
        The welfare that each server has based on the selections of price and
        offloading at the end of the timeslot

    '''

    welfare = (1-fs)*prices*bytes_to_server - c*bytes_to_server

    return welfare

def calculate_user_utility(b, server_selected, prices, k, l, a, **params):
    '''
    Calculates the utility of users at the end of the timeslot

    Parameters
    ----------

    b: 1-D array
        offloading data each user has decided to send on the current
        iteration
    server_selected: 1-D array
        list containing the server to which each user is associated
    prices: 1-D array
        Set the new prices of the servers
    k: int
        parameter of the user's satisfaction function
    l: int
        parameter of the user's satisfaction function
    a: 1-D array
        parameter that reflects users' dynamic behavior to spen more money
        in order to buy computing support from the MEC servers

    Returns
    -------

    utility: 1-D array
        The utility that each user has based on the selections of bytes offloaded
        at the end of the timeslot

    '''
    # Sum of all best responses
    B = np.sum(b)
    # Best response of all users except the user
    B_minus_u = B - b

    # price paid by user based on server's price
    paid = prices[tuple([server_selected])]

    ru = b / B_minus_u
    utility = k*np.log(1+l*ru) - a*paid*ru

    return utility
