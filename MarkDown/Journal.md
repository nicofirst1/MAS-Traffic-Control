# Useful Links

- [Flow, Sumo, RLlib Installation](https://flow.readthedocs.io/en/latest/flow_setup.html#local-installation-of-flow)
- [Flow Documentation](https://flow.readthedocs.io/en/latest/)
- [More Flow documentation and MAS](https://flow-project.github.io/tutorial.html)
- [TraCi documentation](https://sumo.dlr.de/pydoc/traci.html)
- [Ray docs](https://ray.readthedocs.io/en/latest/index.html)
- [Ray repo](https://github.com/ray-project/ray)
- [SUMO documentation](http://sumo.sourceforge.net/userdoc/index.html)
- [SUMO repo](https://github.com/eclipse/sumo)

# TODO

## Starting

1. Install [Flow **dependencies**, Sumo, RLlib](https://flow.readthedocs.io/en/latest/flow_setup.html#local-installation-of-flow)
2. BEWARE do not install flow in your python environment, we have a local copy of the repo in [here](../flow) that needs to be changed.
3. Complete tutorials in [FLOW](https://github.com/flow-project/flow/tree/master/tutorials), especially (0,1,3,5,6,8,11)

## Project

### Network : completed

We can either import map with [OpenStreetMap](https://github.com/flow-project/flow/blob/master/tutorials/tutorial06_osm.ipynb)
or create a custom one with [Scenario](https://github.com/flow-project/flow/blob/master/tutorials/tutorial05_scenarios.ipynb).
 
- Starting with a custom grid map [X]
- Importing scenario from openmap [X]
- Use lust scenario without traffic lights: not possible, switching to OSM networks
- Set inflows from random starting edges in the OSM network [X]
- Add GroningenOSM to the map_utils [x]

#### Premade netwroks
We can import a pre-made network as in [tutorial 4](../FlowMas/Tutorials/4.5_ImportedScenario.py), here's a list:
- [Monaco](https://github.com/lcodeca/MoSTScenario)
- [Lust](https://github.com/lcodeca/LuSTScenario)

This approach has been discarded since there is no easy way to remove traffic lights (network geometry) form this imported scenarios. Using OSM instead.

#### Router
We could use a custom router to choose random direction in the grid.

- Create a router which is like MinicityRouter but makes car exit the map more often []



### Environment
Check out the [environment tutorial](https://github.com/flow-project/flow/blob/master/tutorials/tutorial08_environments.ipynb)
for this part. This part covers the Autonomous agents using RL.

The custom environments must be placed in the [envs dir](flow/envs/multiagent) and you should add it to the [init](flow/envs/multiagent/__init__.py) file.
There is already a [customRL Agent](flow/envs/multiagent/customRL.py) which can be modified as you please. 

I advise yuo to use the [third tutorial](FlowMas/Tutorials/3_GridMapCustomRL.py) to implement the agent (remember to set the DEGUB option to true in the 
[Parameter file](FlowMas/utils/parameters.py) ) and, when you are ready, you can train it on the [simulation](FlowMas/simulation.py). 

For every custom agent the following function must be implemented:

#### Action space (using gym)
Action space is used to tell the Agent it what can/cannot do. Notice that deceleration and acceleration are considered just one param
- __Deceleration__: using comfortable deceleration rate at 3.5 m/s^2 as stated [here](http://ijtte.com/uploads/2012-10-01/5ebd8343-9b9c-b1d4IJTTE%20vol2%20no3%20(7).pdf)
- __Acceleration__: using 10m/s^2 (ferrari acceleration rate), should look into this [wiki link](https://en.wikipedia.org/wiki/G-force#Horizontal) which states that comfortable acceleration for 10 seconds is 20g (200m/s^2) and 10g for 1 minute
- __Lane_changing__: todo

#### Observable space
Define what cars know about each other (turning direction), if you go by neighbors check out *getNeighbors* in the [TraCi documentation](https://sumo.dlr.de/pydoc/traci.html)

Note that each observation should be scaled 0-1
            
Current Observation:
1) agent speed
2) difference between lead speed and agent
3) distance from leader
4) difference between agent speed and follower
5) distance from follower
6) number of neighbors (not scaled obv)
7) average neighbors speed
8) average neighbors acceleration


#### Reward

The current reward is the sum of the following params:

- __Cooperative__: (system_delay + system_standstill_time) * cooperative_weight
- __Selfish__: agent_specific_delay
- __Scaled jerk__: the lower the better
    
#### Modifying flow/core/kernel/vehicle/traci.py
If you wish to add more functions to the traci file you need to look into the [Vehicle file](/anaconda3/envs/dmas/lib/python3.6/site-packages/traci/_vehicle.py) which can be found 
inside your conda envs, for example mine is in:

`/anaconda3/envs/dmas/lib/python3.6/site-packages/traci/_vehicle.py`

#### Related papers
- [Reward function for accelerated learning](http://www.sci.brooklyn.cuny.edu/~sklar/teaching/boston-college/s01/mc375/ml94.pdf)
- [1Safe, Efficient, and Comfortable Velocity Controlbased on Reinforcement Learning forAutonomous Driving](https://arxiv.org/pdf/1902.00089.pdf)