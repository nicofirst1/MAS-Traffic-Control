# the scenario name
from copy import deepcopy

from FlowMas.utils.parameters import Params
from flow.controllers import IDMController, GridRouter
from flow.core.experiment import Experiment
from flow.core.params import VehicleParams, NetParams, InitialConfig, TrafficLightParams, SumoParams, EnvParams
from flow.envs import TestEnv
from flow.envs.traffic_light_grid import ADDITIONAL_ENV_PARAMS
from flow.networks.traffic_light_grid import ADDITIONAL_NET_PARAMS
from flow.scenarios import TrafficLightGridScenario

##############################
#      Vehicle Params
##############################

# vehicle params to take care of all the vehicles
vehicles = VehicleParams()
# number of human drivers
human_num = 200
# add human drivers with premade controllers/routers
vehicles.add("human",
             acceleration_controller=(IDMController, {}),
             routing_controller=(GridRouter, {}),
             num_vehicles=human_num)

##############################
#      NET Params
##############################

# Setting grid measures
additional_net_params = deepcopy(ADDITIONAL_NET_PARAMS)
additional_net_params['grid_array']['inner_length'] = 500
additional_net_params['grid_array']['long_length'] = 500
additional_net_params['grid_array']['short_length'] = 500
additional_net_params['traffic_lights'] = False

# standard stuff, check it out in the tutorial
net_params = NetParams(additional_params=additional_net_params)

##############################
#      Other Params
##############################

initial_config = InitialConfig(spacing="custom", perturbation=1)

sumo_params = SumoParams(sim_step=0.1, render=True, emission_path=Params.DATA_DIR)

additional_env_params = deepcopy(ADDITIONAL_ENV_PARAMS)
env_params = EnvParams(additional_params=additional_env_params)

##############################
#   Scenario Initialization
##############################
scenario = TrafficLightGridScenario(name="grid_tutorial",
                                    vehicles=vehicles,
                                    net_params=net_params,
                                    initial_config=initial_config,
                                    traffic_lights=TrafficLightParams())

##############################
#    Env/Exp creation
##############################
# create the environment object
env = TestEnv(env_params, sumo_params, scenario)

# create the experiment object
exp = Experiment(env)

# run the experiment for a set number of rollouts / time steps
_ = exp.run(1, 3000)
