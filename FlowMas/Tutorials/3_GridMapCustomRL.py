from copy import deepcopy

import ray
from ray.tune import register_env, run_experiments

from FlowMas.utils.parameters import Params
from FlowMas.utils.train_utils import get_default_config
from flow.controllers import IDMController, RLController
from flow.controllers.routing_controllers import GridRouter
from flow.core.params import SumoParams, EnvParams, NetParams, InitialConfig, CustomVehicleParams
from flow.core.params import TrafficLightParams
from flow.envs.multiagent.customRL import ADDITIONAL_ENV_PARAMS
from flow.networks.traffic_light_grid import ADDITIONAL_NET_PARAMS
from flow.scenarios.traffic_light_grid import TrafficLightGridNetwork
from flow.utils.registry import make_create_env

########################
#      VEHICLES
########################


# vehicle params to take care of all the vehicles
vehicles = CustomVehicleParams()
# number of human drivers
human_num = 100
RL_num = 50

# add human drivers with premade controllers/routers
vehicles.add("human",
             acceleration_controller=(IDMController, {}),
             routing_controller=(GridRouter, {}),
             num_vehicles=human_num)

# add RL agents with premade controller
# add coop agents
vehicles.add(
    "RL_coop",
    acceleration_controller=(RLController, {}),
    routing_controller=(GridRouter, {}),
    num_vehicles=RL_num,
    cooperative_weight=0.7
)

# add selfish agent
vehicles.add(
    "RL_selfish",
    acceleration_controller=(RLController, {}),
    routing_controller=(GridRouter, {}),
    num_vehicles=1,
    cooperative_weight=0.1
)

########################
#       ENV PARAM
########################

HORIZON = 1500  # the duration of one episode (during which the RL-agent acquire data).
additional_env_params = deepcopy(ADDITIONAL_ENV_PARAMS)
# the reward parameters for the acceleration


# initializing env params, since env is just Test there will be no learning, but the procedure is the same
env_params = EnvParams(additional_params=additional_env_params, horizon=HORIZON, sims_per_step=5, )

########################
#       NET PARAM
########################

# additional parameters for network (map geometry)
# you should always copy the original one and extend it
additional_net_params = ADDITIONAL_NET_PARAMS.copy()

# defining inflow parameters, see later
additional_net_params["merge_lanes"] = 1
additional_net_params["highway_lanes"] = 1
additional_net_params["pre_merge_length"] = 500
additional_net_params["post_merge_length"] = 100
additional_net_params["merge_length"] = 200

# defining geometry
additional_net_params['grid_array']['inner_length'] = 500
additional_net_params['grid_array']['long_length'] = 500
additional_net_params['grid_array']['short_length'] = 500
additional_net_params['traffic_lights'] = False  # setting traffic lights to false

# standard stuff, check it out in the tutorial
net_params = NetParams(additional_params=additional_net_params, )

# create the scenario object
scenario = TrafficLightGridNetwork(name="grid_example",  # just the scenario name
                                   vehicles=vehicles,
                                   net_params=net_params,
                                   initial_config=InitialConfig(spacing="custom", perturbation=1),
                                   # configuration for initial position of cars
                                   traffic_lights=TrafficLightParams()
                                   # We still need to specify this since the environments needs it
                                   )
########################
#       GENERAL PARAM
########################
# defining a general dictionary containing every configuration ,
# this will be passed to the gym to make the trainable environment
params = dict(
    # name of the experiment
    exp_tag="customRL_grid",

    # name of the flow environment the experiment is running on
    env_name="CustoMultiRL",

    # name of the network class the experiment is running on
    network="TrafficLightGridNetwork",

    # simulator that is used by the experiment
    simulator='traci',

    # sumo-related parameters (see flow.core.params.SumoParams)
    sim=SumoParams(
        sim_step=0.2,
        render=False,  # no renderer will be displayed for training, this is for speed up
        restart_instance=True,
        emission_path=Params.DATA_DIR,
    ),

    # environment related parameters (see flow.core.params.EnvParams)
    env=env_params,

    # network-related parameters (see flow.core.params.NetParams and the
    # network's documentation or ADDITIONAL_NET_PARAMS component)
    net=net_params,

    # vehicles to be placed in the network at the start of a rollout (see
    # flow.core.params.VehicleParams)
    veh=vehicles,

    # parameters specifying the positioning of vehicles upon initialization/
    # reset (see flow.core.params.InitialConfig)
    initial=InitialConfig(spacing="custom"),
)

########################
#  ENV CREATION
########################

# define new trainable enviroment
create_env, gym_name = make_create_env(params=params, version=0)

# get default config for ppo
ppo_config = get_default_config( params)

# Register as rllib env
register_env(gym_name, create_env)

########################
#  START OF TRAINING
########################
ray.init(num_cpus=Params.n_cpus, local_mode=Params.debug)  # use local mode when debugging, remove it for performance increase

# defining dictionary for the experiment
experiment_params = dict(

    run="PPO",  # must be the same as the default config
    env=gym_name,
    config={**ppo_config},
    checkpoint_freq=20,
    checkpoint_at_end=True,
    max_failures=999,
    stop={"training_iteration": 200, },  # stop conditions

)
# weird thing the function wats
experiment_params = {params["exp_tag"]: experiment_params}

# running the experiment
trials = run_experiments(experiment_params)
