In this directory custom tutorial are available. Each one moving a step forward to the final project.

- [1_GridMapNoLights.py](FlowMas/Tutorials/1_GridMapNoLights.py) setup a grid world with only human. Priority is given to the vertical lanes.
- [2_GridMapNoLightsRL.py](FlowMas/Tutorials/2_GridMapNoLightsRL.py), Uses the same world as before, but introduces an Autonomous Agent [AA] which can be trained using the [RLlib](https://flow.readthedocs.io/en/latest/flow_setup.html#optional-install-ray-rllib) library.
- [3_GridMapCustomRL.py](FlowMas/Tutorials/3_GridMapCustomRL.py), Using [Custom RL evnviroment](flow/envs/multiagent/customRL.py) to train an agent in the grid world.
- [4_ImportedOSM.py](FlowMas/Tutorials/5_ImportedMapInflow.py), Importing custom [OpenStreetMap networks](https://sumo.dlr.de/docs/Tools/Import/OSM.html).
- [5_ImportedOsmInflow.py](FlowMas/Tutorials/5_ImportedOsmInflow.py), Using the OSM imported in tutorial 4 with [inflows](https://github.com/flow-project/flow/blob/master/tutorials/tutorial11_inflows.ipynb).
