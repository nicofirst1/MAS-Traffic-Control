# Useful Links

- [Flow, Sumo, RLlib Installation](https://flow.readthedocs.io/en/latest/flow_setup.html#local-installation-of-flow)
- [Flow Documentation](https://flow.readthedocs.io/en/latest/)
- [More documentation and MAS](https://flow-project.github.io/tutorial.html)

# TODO

## Starting

1. Install [Flow, Sumo, RLlib](https://flow.readthedocs.io/en/latest/flow_setup.html#local-installation-of-flow)
2. Complete tutorials in [FLOW](https://github.com/flow-project/flow/tree/master/tutorials), especially (0,1,3,5,6,8,11)

## Project

### Scenarios

We can either import map with [OpenStreetMap](https://github.com/flow-project/flow/blob/master/tutorials/tutorial06_osm.ipynb)
or create a custom one with [Scenario](https://github.com/flow-project/flow/blob/master/tutorials/tutorial05_scenarios.ipynb).
 
- Starting with a custom grid map
    - Define right privilege []
- Importing scenario from openmap

### Environment
Check out the [environment tutorial](https://github.com/flow-project/flow/blob/master/tutorials/tutorial08_environments.ipynb)
for this part. This part covers the Autonomous agents using RL.

Here we need to specify the:
- Action space (using gym)
    - Aks/give/take priority 
- Observable space
    - define what cars know about each other (turning direction)
- Reward
    - Driving time
    - Total driving time * weighed 
## Problems

### - Could not connect to TraCI

Error: ` server at localhost:58127 [Errno 61] Connection refused`

Solution: wait, as written [here](https://stackoverflow.com/questions/40362275/using-sumo-and-traci-could-not-connect-to-traci-server-61)

### - No module named 'rllab'

Error: `ModuleNotFoundError: No module named 'rllab'`

Solution: You must install [rllab](https://github.com/rll/rllab) with the following commands:

- `git clone https://github.com/rll/rllab`
- `cd rllab`
- `source activate 'YourEnvName'`
- `python setup.py install`

Check out [this](https://gist.github.com/yuanzhaoYZ/15bb640e1751da163d6a01675d54825f) for installation with conda
and [this](https://rllab.readthedocs.io/en/latest/user/installation.html) for installation with custom environment.