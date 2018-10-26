'''
Server selection - Learning system functions
'''

import numpy as np

from runparams import *

def server_selection(probabilities):
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

def update_probabilities(probabilities, server_selected, b, all_bytes_to_server, all_fs):
    '''
    Update action probabilities of users on choosing a server

    Parameters
    ----------

    probabilities: 2-D array
        The probabilities that the user will select the specific server
    server_selected: 1-D array
        list containing the server to which each user is associated
    b: 1-D array
        offloading data each user had decided to send
    all_bytes_to_server: 2-D array
        The number of bytes the users have offloaded to the specific server
        up to now
    all_fs: 2-D array
        The discount the servers have offered up to now

    Returns
    -------

    probabilities: 2-D array
        The new probabilities that the user will select the specific server
    '''

    # calculate PAR
    # use np.divide to handle cases where b=0
    a = np.max(all_bytes_to_server, axis=0)
    b = np.mean(all_bytes_to_server, axis=0)
    PAR = np.divide(a, b, out=np.zeros_like(a), where=b!=0)

    # calculate "penetration"
    penetration = np.sum(all_bytes_to_server, axis=0)/np.sum(all_bytes_to_server)

    # use np.divide to handle cases where PAR=0
    Rs = np.sum(all_fs, axis=0) * np.divide(1,PAR, out=np.zeros_like(PAR), where=PAR!=0) * penetration

    reward = Rs/np.sum(Rs)

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
