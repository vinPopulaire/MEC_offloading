# -*- coding: utf-8 -*-
"""
    MEC_offloading.plots_for_paper
    ~~~~~~~~~~~~~~~~~~~~~~~~~

    Generate comparative plots for the MEC_offloading

    :copyright: (c) 2018 by Giorgos Mitsis.
    :license: MIT License, see LICENSE for more details.
"""

import itertools
import dill
import numpy as np

import numpy as np
import matplotlib.pyplot as plt

from create_plots import *

SAVE_FIGS = True

# different cases

# Select which case to run
cases = [{"users": "hetero", "servers": "hetero", "offload": "dyn"}, {"users": "hetero", "servers": "hetero", "offload": "25"}, {"users": "hetero", "servers": "hetero", "offload": "58.6"}, {"users": "hetero", "servers": "hetero", "offload": "100"}]

results = {}
params = {}
keys = []
a = []

for case in cases:

    key = case["users"] + "_" + case["servers"] + "_offload_" + case["offload"]
    keys.append(key)
    infile = "saved_runs/parameters/" + case["users"] + "_" + case["servers"] + "_lr_" + "0.20"

    with open(infile, 'rb') as in_strm:
        params[key] = dill.load(in_strm)

    a.append(params[key]["a"])

    infile = "saved_runs/results/" + key + "_lr_" + "0.20"

    with open(infile, 'rb') as in_strm:
        results[key] = dill.load(in_strm)

# if not np.all(a == a[1]):
#     raise ValueError("Parameters are not equal for different cases")

color_sequence = ['#1f77b4', '#aec7e8', '#ffbb78', '#2ca02c', '#c0c0c0', '#ff00ff', '#00ffff', '#ffff00']

index = 0
offload = ["dynamic offloading", "25% offloading", "58.6% offloading", "100% offloading"]
suptitle = "Average servers' welfare for different cases"
fig, ax = setup_plots(suptitle)

for item in ([ax.title, ax.xaxis.label, ax.yaxis.label]):
    item.set_fontsize(30)
for item in (ax.get_xticklabels() + ax.get_yticklabels()):
    item.set_fontsize(26)
    item.set_fontweight("bold")
font = {'weight' : 'bold'}
matplotlib.rc('font', **font)

# set offset so that text on the figures does not collide
y_offset = [-700, 0, 300, 0]
for key in keys:
    average_welfare = np.mean(results[key]["all_server_welfare"][:results[key]["median_timeslots"]], axis=1)

    plt.plot(average_welfare, lw=5, color=color_sequence[index])

    y_pos = average_welfare[-1]
    plt.text(len(average_welfare) + 5, y_pos+y_offset[index], offload[index], fontsize=24, color=color_sequence[index])
    index += 1

xlabel = "timeslots"
ylabel = "servers' welfare"
plt.xlabel(xlabel, fontweight='bold')
plt.ylabel(ylabel, fontweight='bold')
path_name = "all_server_welfare"
if SAVE_FIGS == True:
    plt.savefig("plots/" + path_name + ".png")
plt.show(block=False)

index = 0
suptitle = "Average users' utility for different cases"
fig, ax = setup_plots(suptitle)
for key in keys:
    average_utility = np.mean(results[key]["all_user_utility"][:results[key]["median_timeslots"]], axis=1)

    plt.plot(average_utility, lw=5, color=color_sequence[index])

    y_pos = average_utility[-1]
    plt.text(len(average_utility) + 5, y_pos, offload[index], fontsize=24, color=color_sequence[index])
    index += 1

xlabel = "timeslots"
ylabel = "users' utility"
plt.xlabel(xlabel, fontweight='bold')
plt.ylabel(ylabel, fontweight='bold')
path_name = "all_user_utility"
if SAVE_FIGS == True:
    plt.savefig("plots/" + path_name + ".png")
plt.show(block=False)

# different learning rates

# Select which case to run
case = {"users": "hetero", "servers": "hetero"}
learning_rates = ["0.10", "0.20", "0.30", "0.40", "0.50"]

results = {}
params = {}
keys = []
a = []
for learning_rate in learning_rates:

    key = case["users"] + "_" + case["servers"] + "_lr_" + learning_rate
    keys.append(key)
    infile = "saved_runs/parameters/" + key

    with open(infile, 'rb') as in_strm:
        params[key] = dill.load(in_strm)

    a.append(params[key]["a"])

    infile = "saved_runs/results/" + key

    with open(infile, 'rb') as in_strm:
        results[key] = dill.load(in_strm)

if not np.all(a == a[1]):
    raise ValueError("Parameters are not equal for different cases")

color_sequence = ['#1f77b4', '#aec7e8', '#ff7f0e', '#ffbb78', '#2ca02c']

index = 0
suptitle = "Average servers' welfare for different learning rates"
fig, ax = setup_plots(suptitle)

for item in ([ax.title, ax.xaxis.label, ax.yaxis.label]):
    item.set_fontsize(30)
for item in (ax.get_xticklabels() + ax.get_yticklabels()):
    item.set_fontsize(26)
    item.set_fontweight("bold")
font = {'weight' : 'bold'}
matplotlib.rc('font', **font)

for key in keys:
    average_welfare = np.mean(results[key]["all_server_welfare"][:results[key]["median_timeslots"]], axis=1)

    plt.plot(average_welfare, lw=5, color=color_sequence[index])

    y_pos = average_welfare[-1]
    name = "b = " + key[-4:]
    plt.text(len(average_welfare) + 5, y_pos, name, fontsize=24, color=color_sequence[index])
    index += 1

xlabel = "timeslots"
ylabel = "servers' welfare"
plt.xlabel(xlabel, fontweight='bold')
plt.ylabel(ylabel, fontweight='bold')
path_name = "all_server_welfare_different_learning_rates"
if SAVE_FIGS == True:
    plt.savefig("plots/" + path_name + ".png")
plt.show(block=False)

index = 0
suptitle = "Average users' utility for different cases"
fig, ax = setup_plots(suptitle)

for item in ([ax.title, ax.xaxis.label, ax.yaxis.label]):
    item.set_fontsize(30)
for item in (ax.get_xticklabels() + ax.get_yticklabels()):
    item.set_fontsize(26)
    item.set_fontweight("bold")
font = {'weight' : 'bold'}
matplotlib.rc('font', **font)

for key in keys:
    average_utility = np.mean(results[key]["all_user_utility"][:results[key]["median_timeslots"]], axis=1)

    plt.plot(average_utility, lw=5, color=color_sequence[index])

    y_pos = average_utility[-1]
    name = "b = " + key[-4:]
    plt.text(len(average_utility) + 5, y_pos, name, fontsize=24, color=color_sequence[index])
    index += 1

xlabel = "timeslots"
ylabel = "users' utility"
plt.xlabel(xlabel, fontweight='bold')
plt.ylabel(ylabel, fontweight='bold')
path_name = "all_user_utility_different_learning_rates"
if SAVE_FIGS == True:
    plt.savefig("plots/" + path_name + ".png")
plt.show(block=False)

if SAVE_FIGS == False:
    plt.show()
