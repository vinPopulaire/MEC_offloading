'''
Server selection - Learning system functions
'''

import numpy as np

def server_selection(probabilities, U, S, **params):
    '''
    Each user selects a server to whom it will offload the data.

    Parameters
    ----------

    probabilities: 1-D array
        The probabilities that the user will select the specific server

    Returns
    -------

    servers: 1-D array
        list containing the server to which each user is associated
    '''

    # Each user selects the server to which he will offload his data based
    # on the probabilities distribution he has
    servers = np.array([np.random.choice(np.arange(S), replace=True, p=probabilities[user])
        for user in np.arange(U)])

    return servers

def all_users_sure(probabilities):
    '''
    Check if all users are certain of the selection they made on the server

    Parameters
    ----------

    probabilities: 2-D array
        The probabilities that each user will select the specific server

    Returns
    -------

    Boolean
        Boolean on whether all users are sure of the selected server or not
    '''

    # check if all rows have at least one server with probability > 0.9
    if np.all(np.max(probabilities, axis=1) > 0.9):
        return True
    return False

def calculate_competitiveness(all_bytes_to_server, all_fs, all_prices, U, S, b_max,  **params):
    '''
    Calculate the competitiveness score Rs used on the update function

    Parameters
    ----------

    all_bytes_to_server: 2-D array
        The number of bytes the users have offloaded to the specific server
        up to now
    all_fs: 2-D array
        The discount the servers have offered up to now
    all_prices: 2-D array
        The prices the servers have set up to now
    U: int
        Number of users
    S: int
        Number of servers
    b_max: int
        Maximum number of bits that the user is willing to offload

    Returns
    -------

    Rs: 1-D array
        the competitiveness score of each server
    relative_price: 1-D array
        the relative pricing of each server
    congestion: 1-D array
        the congestion of each server
    penetration: 1-D array
        the penetration of each server on the offloading market
    '''

    # calculate relative pricing
    denominator = all_prices[-1] - all_fs[-1]*all_prices[-1]
    numerator = np.sum(denominator)/S
    relative_price = numerator / denominator

    # calculate congestion
    # set B_max of each server to be able to handle all traffic
    tmp1 = all_bytes_to_server[-1]
    tmp2 = b_max * U
    congestion = np.power((tmp1/tmp2),5)
    congestion[congestion==0] = 0.001 # to avoid division by zero

    # calculate "penetration"
    # use np.divide to handle cases where tmp2=0
    tmp1 = np.sum(all_bytes_to_server, axis=0)
    tmp2 = np.sum(all_bytes_to_server)
    penetration = np.divide(tmp1, tmp2, out=np.zeros_like(tmp1), where=tmp2!=0)

    Rs = relative_price * 1/congestion * penetration

    return Rs,relative_price,congestion,penetration

def update_probabilities(Rs, probabilities, server_selected, b, learning_rate,  **params):
    '''
    Update action probabilities of users on choosing a server

    Parameters
    ----------

    Rs: 1-D array
        the competitiveness score of each server
    probabilities: 2-D array
        The probabilities that the user will select the specific server
    server_selected: 1-D array
        list containing the server to which each user is associated
    b: 1-D array
        offloading data each user had decided to send

    Returns
    -------

    probabilities: 2-D array
        The new probabilities that the user will select the specific server
    '''

    # use np.divide to handle cases where sum(Rs)=0
    tmp1 = Rs
    tmp2 = np.sum(Rs)
    reward = np.divide(tmp1, tmp2, out=np.zeros_like(tmp1), where=tmp2!=0)

    # create second part of probabilities update
    Pr = np.copy(probabilities)

    Pr[np.arange(Pr.shape[0]), server_selected] = -(1-Pr[np.arange(Pr.shape[0]), server_selected])
    Pr = -Pr*learning_rate

    tmp = reward[tuple([server_selected])]
    # change tmp row array to column array
    tmp = tmp[:, np.newaxis]

    Pr = Pr * tmp

    probabilities = probabilities + Pr

    return probabilities
