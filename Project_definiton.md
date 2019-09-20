# Introduction

Autonomous car  are being introduces in various countries. In 2019 a total of 1,400 autonomous car have been registered in the US only.
With the rising of this kind of technologies some research is needed to study and simulate the interaction between autonomous car  and humans.

## State of the art

In "Simulating Autonomous and Human-Driven Vehicles in Traffic Intersections" the authors study the interaction between Autonomous Agents [AA] and Human Agents [HA], using different field of views and reaction times for both type of drivers. However, their simulation shows barely any difference between both types of drivers, from which they conclude that these two properties field of view and reaction time are not the most distinctive properties.

## New Idea

Our idea is to investigate different behavior for AA in this context. Specifically we want to model a context in which there are self-centeredness vs cooperative agents.
Self-centered agents would behave more Humans Agents [HA] (no communication whatsoever) but with faster reflexes and wider FOVs.

## Environment
Our environment would be a simulation, using the Flow framework (https://github.com/flow-project/flow), a python framework for traffic modeling. There will be no traffic agents, thus no traffic light, so that in an intersection the AA can either take priority (if it can) or give it to other AAs (by means of communication).

## Agents
Each AA will have a reward function which aims to decrease the driving time. Moreover there will be an addiction to reward function taking into account a weighted total driving time, that is the driving time of each AA. The weight let us decide the selfishness of the agent.

Each HA will be treated like a fully self-centered AA, which can occasionally break the rules (not giving priority at intersections).

## Learning
For each AA we will implement the communication part as to have a finite state of action so that each agent can learn how to behave using Reinforcement Learning [RL].


## Communication
For this kind of task we need to build a communication system so that AAs can exchange information (maybe locally for optimization?). We will have communication actions as:
- Give priority
- Request priority

And possibly others.



* Main Question*
- Is communication better than self-interest?
- How do HAs affect AAs in their performance?
- Will AAs develop a way to deal with HAs?
- How does introducing different kind of communication changes the system behavior?

We can tune parameters such as:
- Communication incentive, to study how the performance de/increases
- HAs number, to simulate realistic environments.

* More Referencs*
- Traffic Intersections of the Future (http://new.aaai.org/Papers/AAAI/2006/AAAI06-258.pdf)
- Developing a Python Reinforcement Learning Library forTraffic Simulation (http://ala2017.it.nuigalway.ie/papers/ALA2017_Ramos.pdf)
- CityFlow: A Multi-Agent Reinforcement Learning Environmentfor Large Scale City Traffic Scenario (https://arxiv.org/pdf/1905.05217.pdf)