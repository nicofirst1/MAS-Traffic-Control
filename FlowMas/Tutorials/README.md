In this dir custom tutorial are available. Each one moving a step forward to the final project.

0. [1_GridMapNoLights.py](FlowMas/Tutorials/1_GridMapNoLights.py) setup a grid world with only human. Priority is given to the vertical lanes.
1. [2_GridMapNoLightsRL.py](FlowMas/Tutorials/2_GridMapNoLightsRL.py), NOT WORKING ... uses the same world as before, but introduces an Autonomous Agent [AA] which can be trained using the [RLlib](https://flow.readthedocs.io/en/latest/flow_setup.html#optional-install-ray-rllib) library.
2. [3_GridMapCustomRL.py](FlowMas/Tutorials/3_GridMapCustomRL.py), Using [Custom RL evnviroment](flow/envs/multiagent/customRL.py) to train an agent in the grid world.
3. [4_ImportedMap.py](FlowMas/Tutorials/4_ImportedMap.py), Importing the LuSTScenario and removing traffic lights from it.
3. [5_ImportedMapInflow.py](FlowMas/Tutorials/5_ImportedMapInflow.py), Using previous imported scenario with inflows