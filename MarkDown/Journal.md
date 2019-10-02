# Useful Links

- [Flow, Sumo, RLlib Installation](https://flow.readthedocs.io/en/latest/flow_setup.html#local-installation-of-flow)
- [Flow Documentation](https://flow.readthedocs.io/en/latest/)
- [Flow tutorials](https://github.com/flow-project/flow/tree/master/tutorials)
- [More Flow documentation and MAS](https://flow-project.github.io/tutorial.html)
- [TraCi documentation](https://sumo.dlr.de/pydoc/traci.html)
- [Ray docs](https://ray.readthedocs.io/en/latest/index.html)
- [Ray repo](https://github.com/ray-project/ray)
- [SUMO documentation](http://sumo.sourceforge.net/userdoc/index.html)
- [SUMO repo](https://github.com/eclipse/sumo)

# TODO

- Change echo for "conda activate dmas" to support "source activate dmas"
- Update README.md to include the activation of the env, and the approval of uninstalling flow
- Update README.md to include running the goal simulation.py
- Expand README.md to specify an appropriate OS (Ubuntu 18.04)

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

### Training

- Use gpu support []
- Print debug infos and training progress []


## Research 
This section will be about research topics we will add to the project. For every issue we will address a paper with a brief description of 
how the issue can be addressed as well as a reference to the paper itself.


###  Training
For this kind of issue take a look at the [ray's tune](https://ray.readthedocs.io/en/latest/tune.html#getting-started) framework,
which is the one we're using right now.

We need something with the following characteristic:

#### Compatible with continuous action space 

- No Q-learning such as DQN, Actor/Critic is better.
- IMPALA cannot be used since lack implementation in ray ([here](https://github.com/ray-project/ray/issues/2777))


#### Working in a decentralized fashion
APEX  seems good

#### Model based  
From [our paper](https://scholar.googleusercontent.com/scholar?q=cache:6bZ1QS39AvkJ:scholar.google.com/+mas+rl+traffic&hl=en&as_sdt=0,5&as_vis=1)
and [more](https://scholar.googleusercontent.com/scholar?q=cache:0ZLOVBrS7csJ:scholar.google.com/+mas+rl+traffic&hl=en&as_sdt=0,5&as_vis=1)  
MODEL based approaches seems the one working better in MAS envs.
So we can exclude the following:

- PPO
- DQN 
- PG
- A2C
- A3C
- DDPG
- TD3
- APEX

#### Policy Based
[More here](https://www.quora.com/Why-does-the-policy-gradient-method-have-a-high-variance). Main points:
- No good when reward is zero -> high baseline for reward (must be small)

##### PPO [X]
[More here](https://medium.com/@jonathan_hui/rl-proximal-policy-optimization-ppo-explained-77f014ec3f12). Main points:
- Formalizes the constraint as a penalty in the objective function. 
- Can use a first-order optimizer.


##### PG [X]
[More here](https://medium.com/@jonathan_hui/rl-policy-gradients-explained-9b13b688b146). Main points:
- Makes actions with high rewards more likely, or vice versa. 

Naive , task to hard for this simplistic approach.

##### DDPG [X]
[More here](https://towardsdatascience.com/deep-deterministic-policy-gradients-explained-2d94655a9b7b). Main points:

- Actor directly maps states to actions (the output of the network directly the output) instead of outputting the probability distribution across a discrete action space.
- Improve stability in learning

##### TD3 [X]
[More here](https://spinningup.openai.com/en/latest/algorithms/td3.html)
Trick One: Clipped Double-Q Learning. TD3 learns two Q-functions instead of one (hence “twin”), and uses the smaller of the two Q-values to form the targets in the Bellman error loss functions.

Trick Two: “Delayed” Policy Updates. TD3 updates the policy (and target networks) less frequently than the Q-function. The paper recommends one policy update for every two Q-function updates.

Trick Three: Target Policy Smoothing. TD3 adds noise to the target action, to make it harder for the policy to exploit Q-function errors by smoothing out Q along changes in action.


#### Actor Critic Methods
Avoids noisy gradients and high variance.
The “Critic” estimates the value function. This could be the action-value (the Q value) or state-value (the V value).
The “Actor” updates the policy distribution in the direction suggested by the Critic (such as with policy gradients).

##### A3C [X]
Introduce by deep mind [here](https://arxiv.org/abs/1602.01783). Main points:

- Implements parallel training where multiple workers in parallel environments independently update a global value function.
- Not proved to be better than A2C

##### A2C [X]
 Main points:
- A2C is like A3C but without the asynchronous part.

##### SAC
[More here](https://spinningup.openai.com/en/latest/algorithms/sac.html). Main points:

- SAC is an off-policy algorithm.
- Used for environments with continuous action spaces.
- Entropy regularization. The policy is trained to maximize a trade-off between expected return and entropy, a measure of randomness in the policy. This has a close connection to the exploration-exploitation trade-off: increasing entropy results in more exploration, which can accelerate learning later on

##### IMPALA [X]
Importance Weighted Actor-Learner Architecture 

- different actors and learners that can collaborate to build knowledge across different domains
- completely independent actors and learners. This simple architecture enables the learner(s) to be accelerated using GPUs and actors to be easily distributed across many machines.
- mitigate the lag between when actions are generated by the actors and when the learner estimates the gradient.
-  efficiently operate in multi-task environments.


##### MARWIL
Exponentially Weighted Imitation Learning for Batched Historical Data. [More here](https://papers.nips.cc/paper/7866-exponentially-weighted-imitation-learning-for-batched-historical-data.pdf).

Main points:
- applicable to problems with complex nonlinear function approximation
- works well with hybrid (discrete and continuous) action space: both acceleration and lane switching
- an be used to learn from data generated by an unknown policy
-  batched historical trajectories.

#### APEX[X]
The algorithm decouples acting from learning:  the actors interact with their own instances of the environment by 
selecting actions according to a shared neural network, and accumulate the resulting experience in a shared experience 
replay memory; the learner replays samples of experience and updates the  neural  network.
The  architecture  relies  on  prioritized  experience  replay  to focus only on the most 
significant data generated by the actors.

[More here](https://openreview.net/pdf?id=H1Dy---0Z). Variations:

- APEX
- APEX_DDPG [X]


#### Search[X]

##### ES [X]
[More here](https://openai.com/blog/evolution-strategies/). Main points:

- ES resembles simple hill-climbing in a high-dimensional space based only on finite differences along a few random directions at each step.


##### ARS [X]
[More here](https://towardsdatascience.com/introduction-to-augmented-random-search-d8d7b55309bd)



#### Other[X]


##### DQN [X]
[More here](https://towardsdatascience.com/cartpole-introduction-to-reinforcement-learning-ed0eb5b58288). Main points:

- DQN is a RL technique that is aimed at choosing the best action for given circumstances (observation).

We wont use it since it is prone to high variance in the training phase.



#### Scheduler
Scheduler is used for schedule training procedures, can parallelize, can take best out of N population. Used for tuning.
- Currently trying [population-based-training](https://deepmind.com/blog/article/population-based-training-neural-networks)

### RL Agent
This subsection is dedicated to the RL agent functions

#### Action space
Action space is continuous since we're using acceleration as output.

#### Observation space
Something

#### Reward function
Ideas

#### Clip action
Pro and cons of the ‘clip action’ function
