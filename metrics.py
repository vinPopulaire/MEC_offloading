'''
Functions to calculate metrics
'''

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
