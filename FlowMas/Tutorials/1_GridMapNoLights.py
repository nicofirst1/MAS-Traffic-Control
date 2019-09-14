
# the scenario name
from flow.controllers import IDMController, GridRouter
from flow.core.experiment import Experiment
from flow.core.params import VehicleParams, NetParams, InitialConfig, TrafficLightParams, SumoParams, EnvParams
from flow.envs import AccelEnv
from flow.envs.traffic_light_grid import ADDITIONAL_ENV_PARAMS
from flow.networks.traffic_light_grid import ADDITIONAL_NET_PARAMS
from flow.scenarios import TrafficLightGridScenario

name = "grid_example"

# vehicle params to take care of all the vehicles
vehicles = VehicleParams()
# number of human drivers
human_num = 200

# add human drivers with premade controllers/routers
vehicles.add("human",
             acceleration_controller=(IDMController, {}),
             routing_controller=(GridRouter, {}),
             num_vehicles=human_num)

# Setting grid measures
ADDITIONAL_NET_PARAMS['grid_array']['inner_length'] = 500
ADDITIONAL_NET_PARAMS['grid_array']['long_length'] = 500
ADDITIONAL_NET_PARAMS['grid_array']['short_length'] = 500
ADDITIONAL_NET_PARAMS['traffic_lights'] = False

# standard stuff, check it out in the tutorial
net_params = NetParams(additional_params=ADDITIONAL_NET_PARAMS)
initial_config = InitialConfig(spacing="custom", perturbation=1)
traffic_lights = TrafficLightParams()
sumo_params = SumoParams(sim_step=0.1, render=True, emission_path='data')
env_params = EnvParams(additional_params=ADDITIONAL_ENV_PARAMS)

# create the scenario object
scenario = TrafficLightGridScenario(name=name,
                                    vehicles=vehicles,
                                    net_params=net_params,
                                    initial_config=initial_config,
                                    traffic_lights=traffic_lights)

# create the environment object
env = AccelEnv(env_params, sumo_params, scenario)

# create the experiment object
exp = Experiment(env)

# run the experiment for a set number of rollouts / time steps
_ = exp.run(1, 3000, convert_to_csv=True)
