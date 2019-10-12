import ray
from ray.tune import register_env, run_experiments

from FlowMas.utils.parameters import Params
from FlowMas.utils.train_utils import get_default_config
from flow.controllers import IDMController, RLController
from flow.controllers.routing_controllers import GridRouter
from flow.core.params import SumoParams, EnvParams, NetParams, InitialConfig
from flow.core.params import TrafficLightParams
from flow.core.params import VehicleParams
from flow.networks.traffic_light_grid import ADDITIONAL_NET_PARAMS
from flow.scenarios.traffic_light_grid import TrafficLightGridNetwork
from flow.utils.registry import make_create_env

##############################
#      Vehicle Params
##############################

# vehicle params to take care of all the vehicles
vehicles = VehicleParams()
# number of human drivers
human_num = 1

# add human drivers with premade controllers/routers
vehicles.add("human",
             acceleration_controller=(IDMController, {}),
             routing_controller=(GridRouter, {}),
             num_vehicles=human_num)

# add RL agent with premade controller
vehicles.add(
    "RL",
    acceleration_controller=(RLController, {}),
    routing_controller=(GridRouter, {}),
    num_vehicles=1,
)

########################
#       ENV PARAM
########################

HORIZON = 1500  # the duration of one episode (during which the RL-agent acquire data).

# the reward parameters for the acceleration
ADDITIONAL_ENV_PARAMS = {
    "max_accel": 1,
    "max_decel": 1,
    "target_velocity": 20,

}

# initializing env params, since env is just Test there will be no learning, but the procedure is the same
env_params = EnvParams(additional_params=ADDITIONAL_ENV_PARAMS, horizon=HORIZON, )

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
    exp_tag="grid_rl_tutorial",

    # name of the flow environment the experiment is running on
    env_name="TestEnv",  # this kind of env does not train anything, check it out in flow.env.testenv

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
config = get_default_config(params)

# Register as rllib env
register_env(gym_name, create_env)

########################
#  START OF TRAINING
########################

ray.init(num_cpus=1, local_mode=True)

# defining dictionary for the experiment
experiment_params = dict(

    run="PPO",  # must be the same as the default config
    env=gym_name,
    config={**config},
    checkpoint_freq=20,
    checkpoint_at_end=True,
    max_failures=999,
    stop={"training_iteration": 200, },  # stop conditions

)

# weird thing the function wats
experiment_params = {params["exp_tag"]: experiment_params}

# running the experiment
trials = run_experiments(experiment_params)
