# -*- coding: utf-8 -*-
"""
    MEC_offloading.generate_aggregated_results
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Generate aggragated results for the MEC_offloading

    :copyright: (c) 2018 by Giorgos Mitsis.
    :license: MIT License, see LICENSE for more details.
"""

import numpy as np
import matplotlib.pyplot as plt
import dill

from create_plots import *

# Select which case to run
cases = [{"users": "hetero", "servers": "hetero"}]

elements = ["all_bytes_offloaded", "all_prices","all_server_welfare", "all_bytes_to_server", "all_Rs", "all_c", "all_fs", "all_congestion", "all_penetration", "all_relative_price", "all_user_utility"]

S = 5
lr = "0.20"
repetitions = 1000

for case in cases:

    key = case["users"] + "_" + case["servers"]

    # infile = "/media/giorgos/My Passport/Programming/MEC offloading/parameters/" + key + "_lr_" + lr
    infile = "saved_runs/parameters/" + key + "_lr_" + lr
    with open(infile, 'rb') as in_strm:
        params = dill.load(in_strm)

    for i in range(repetitions):

        # infile = "/media/giorgos/My Passport/Programming/MEC offloading/results_" + key + "/" + key + "_lr_" + lr + "_rep_" + str(i+1)
        infile = "saved_runs/results/individual/" + key + "_lr_" + lr + "_rep_" + str(i+1)

        with open(infile, 'rb') as in_strm:
            result = dill.load(in_strm)

        if i == 0:
            average_result = result.copy()
            number_of_timeslots = np.ones(len(result["all_bytes_offloaded"]))

            average_result["average_timeslots"] = len(result["all_bytes_offloaded"])
            average_result["median_timeslots"] = [len(result["all_bytes_offloaded"])]

            all_server_selected = result["all_server_selected"]
            average_result["all_server_selected"] = np.empty((0, S), int)
            for row in all_server_selected:
                # the bincount finds how many times each server has been selected
                average_result["all_server_selected"] = np.append(average_result["all_server_selected"], [np.bincount(row, minlength=S)], axis=0)

        else:
            a = result["all_bytes_offloaded"]
            b = average_result["all_bytes_offloaded"]

            average_result["running_time"] += result["running_time"]
            average_result["average_timeslots"] += len(result["all_bytes_offloaded"])
            average_result["median_timeslots"].append(len(result["all_bytes_offloaded"]))

            all_server_selected = result["all_server_selected"]
            tmp = np.empty((0, S), int)
            for row in all_server_selected:
                # the bincount finds how many times each server has been selected
                tmp = np.append(tmp, [np.bincount(row, minlength=S)], axis=0)

            if len(a) < len(b):
                number_of_timeslots[:len(a)] += 1
                for element in elements:
                    c = average_result[element].copy()
                    c[:len(result[element])] += result[element]
                    c[len(result[element]):] += result[element][-1]
                    average_result[element] = c.copy()

                c = average_result["all_server_selected"].copy()
                c[:len(tmp)] += tmp
                c[len(tmp):] += tmp[-1]
                average_result["all_server_selected"] = c.copy()

            else:
                zeros = np.zeros(a.shape[0])
                zeros[:len(number_of_timeslots)] = number_of_timeslots.copy()
                number_of_timeslots = zeros.copy() + 1

                for element in elements:
                    c = result[element].copy()
                    c[:len(average_result[element])] += average_result[element]
                    c[len(average_result[element]):] += average_result[element][-1]
                    average_result[element] = c.copy()

                c = tmp.copy()
                c[:len(average_result["all_server_selected"])] += average_result["all_server_selected"]
                c[len(average_result["all_server_selected"]):] += average_result["all_server_selected"][-1]
                average_result["all_server_selected"] = c.copy()

    average_result["number_of_timeslots"] = number_of_timeslots
    # if I want to average based on number of timeslots I need to divide by number_of_timeslots[:,None]
    average_result["all_bytes_offloaded"] = average_result["all_bytes_offloaded"] / number_of_timeslots[1]
    average_result["all_prices"] = average_result["all_prices"] / number_of_timeslots[1]
    average_result["all_bytes_to_server"] = average_result["all_bytes_to_server"] / number_of_timeslots[1]
    average_result["all_Rs"] = average_result["all_Rs"] / number_of_timeslots[1]
    average_result["all_congestion"] = average_result["all_congestion"] / number_of_timeslots[1]
    average_result["all_penetration"] = average_result["all_penetration"] / number_of_timeslots[1]
    average_result["all_fs"] = average_result["all_fs"] / number_of_timeslots[1]
    average_result["all_c"] = average_result["all_c"] / number_of_timeslots[1]
    average_result["all_relative_price"] = average_result["all_relative_price"] / number_of_timeslots[1]
    average_result["all_server_welfare"] = average_result["all_server_welfare"] / number_of_timeslots[1]
    average_result["all_user_utility"] = average_result["all_user_utility"] / number_of_timeslots[1]
    average_result["all_server_selected"] = average_result["all_server_selected"] / number_of_timeslots[1]
    average_result["running_time"] = average_result["running_time"] / repetitions
    average_result["average_timeslots"] = int(average_result["average_timeslots"] / repetitions)
    average_result["median_timeslots"] = int(np.median(average_result["median_timeslots"]))

    outfile = 'saved_runs/results/' + case["users"] + "_" + case["servers"] + "_lr_" + "{0:.2f}".format(params["learning_rate"])

    with open(outfile , 'wb') as fp:
        dill.dump(average_result, fp)
