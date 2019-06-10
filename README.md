# MEC_offloading
Code for generating Intelligent Dynamic Data Offloading in a Competitive Mobile Edge Computing Market paper's simulation results.
https://www.mdpi.com/1999-5903/11/5/118/pdf

### Abstract

Software Defined Networks (SDN) and Mobile Edge Computing (MEC), capable of dynamically managing and satisfying the end-users computing demands, have emerged as key enabling technologies of 5G networks. In this paper, the joint problem of MEC server selection by the end-users and their optimal data offloading, as well as the optimal price setting by the MEC servers is studied in a multiple MEC servers and multiple end-users environment. The flexibility and programmability offered by the SDN technology, enables the realistic implementation of the proposed framework.
Initially, an SDN controller executes a reinforcement learning framework based on the theory of stochastic learning automata towards enabling the end-users to select a MEC server to offload their data. The discount offered by the MEC server, its congestion and its penetration in terms of serving end-users' computing tasks, and its announced pricing for its computing services are considered in the overall MEC selection process. To determine the end-users' data offloading portion to the selected MEC server, a non-cooperative game among the end-users of each server is formulated and the existence and uniqueness of the corresponding Nash Equilibrium is shown. An optimization problem of maximizing the MEC servers' profit is formulated and solved in order to determine the MEC servers' optimal pricing with respect to their offered computing services and the received offloaded data. To realize the proposed framework, an iterative and low-complexity algorithm is introduced and designed. The performance of the proposed approach is evaluated through modeling and simulation under several scenarios, with both homogeneous and heterogeneous end-users.

### Prerequisites

Clone the repository locally
```
git clone https://github.com/vinPopulaire/MEC_offloading.git
```

Create a python virtual environment
```
virtualenv -p python3 env
source env/bin/activate
```

Install dependacies
```
pip install -r requirements.txt
```

Create folders inside project root folder to store results
```
mkdir saved_runs
mkdir saved_runs/parameters
mkdir saved_runs/results
mdkir saved_runs/results/individual
mkdir plots
```

### Run simulations

Set general parameters of the simulation
```
vim paremeters.py
```

Set cases to run and number of repetitions of the simulation
```
vim simulations.py
```

Run simulation
```
ipython simulation.py
```

### Generate results from multiple runs of the simulation

Set parameters to match the ones you set on the simulations
```
vim generate_aggregated_results.py
```

Run the script for the aggregation of results
```
ipython generate_aggregeted_results.py
```

### Create plots

Set parameters for the generation of plots
```
vim create_plots.py
vim plots_comparative.py
```

Run plot functions to generate the plots used in the paper
```
ipython create_plots.py
ipython plots_comparative.py
```

## Authors

* **Giorgos Mitsis** - [vinpopulaire](https://github.com/vinPopulaire)

## License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details
