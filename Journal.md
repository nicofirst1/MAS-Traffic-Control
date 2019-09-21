# Useful Links

- [Flow, Sumo, RLlib Installation](https://flow.readthedocs.io/en/latest/flow_setup.html#local-installation-of-flow)
- [Flow Documentation](https://flow.readthedocs.io/en/latest/)
- [More Flow documentation and MAS](https://flow-project.github.io/tutorial.html)
- [TraCi documentation](https://sumo.dlr.de/pydoc/traci.html)
- [Ray docs](https://ray.readthedocs.io/en/latest/index.html)
- [Ray repo](https://github.com/ray-project/ray)
- [SUMO documentation](http://sumo.sourceforge.net/userdoc/index.html)

# TODO

## Starting

1. Install [Flow **dependencies**, Sumo, RLlib](https://flow.readthedocs.io/en/latest/flow_setup.html#local-installation-of-flow)
2. BEWARE do not install flow in your python environment, we have a local copy of the repo in [here](flow) that needs to be changed.
3. Complete tutorials in [FLOW](https://github.com/flow-project/flow/tree/master/tutorials), especially (0,1,3,5,6,8,11)

## Project

### Network : completed

We can either import map with [OpenStreetMap](https://github.com/flow-project/flow/blob/master/tutorials/tutorial06_osm.ipynb)
or create a custom one with [Scenario](https://github.com/flow-project/flow/blob/master/tutorials/tutorial05_scenarios.ipynb).
 
- Starting with a custom grid map [X]
- Importing scenario from openmap [X]
- Use lust scenario without traffic lights: not possible, switching to OSM networks
- Set inflows from random starting edges in the OSM network [X]

#### Premade netwroks
We can import a pre-made network as in [tutorial 4](FlowMas/Tutorials/4.5_ImportedScenario.py), here's a list:
- [Monaco](https://github.com/lcodeca/MoSTScenario)
- [Lust](https://github.com/lcodeca/LuSTScenario)

This approach has been discarded since there is no easy way to remove traffic lights (network geometry) form this imported scenarios. Using OSM instead.

#### Router
We could use a custom router to choose random direction in the grid.

- Create a router which is like MinicityRouter but makes car exit the map more often []



### Environment
Check out the [environment tutorial](https://github.com/flow-project/flow/blob/master/tutorials/tutorial08_environments.ipynb)
for this part. This part covers the Autonomous agents using RL.

Here we need to specify the:
- Action space (using gym)
    - Stop 
    - De/accelerate
    
- Observable space
    - Define what cars know about each other (turning direction), if you go by neighbors check out *getNeighbors* in the [TraCi documentation](https://sumo.dlr.de/pydoc/traci.html)
- Reward
    - Driving time
    - Total driving time * weighed 
    
#### Modifying flow/core/kernel/vehicle/traci.py
If you wish to add more functions to the traci file you need to look into the [Vehicle file](/anaconda3/envs/dmas/lib/python3.6/site-packages/traci/_vehicle.py) which can be found 
inside your conda envs, for example mine is in:
`/anaconda3/envs/dmas/lib/python3.6/site-packages/traci/_vehicle.py`
