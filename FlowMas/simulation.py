from copy import deepcopy

# the Experiment class is used for running simulations
import ray
from ray.tune import register_env, run_experiments

from FlowMas.utils.parameters import Params
from FlowMas.utils.general_utils import inflow_random_edges, ppo_default_config
from flow.controllers import IDMController, RLController
from flow.controllers.routing_controllers import MinicityRouter, GridRouter
from flow.core.experiment import Experiment
from flow.core.params import EnvParams, InitialConfig, CustomVehicleParams
from flow.core.params import NetParams
from flow.core.params import SumoParams
# all other imports are standard
from flow.core.params import VehicleParams
# the base network class
from flow.envs import TestEnv
from flow.networks import Network
from flow.networks.osm_map import OSMap
from flow.networks.traffic_light_grid import ADDITIONAL_NET_PARAMS
from flow.envs.multiagent.customRL import ADDITIONAL_ENV_PARAMS
from flow.utils.registry import make_create_env

try:
    from ray.rllib.agents.agent import get_agent_class
except ImportError:
    from ray.rllib.agents.registry import get_agent_class
from flow.core.params import InFlows


# Remove traffic lights
additional_net_params = deepcopy(ADDITIONAL_NET_PARAMS)


########################
#      VEHICLES
########################


# vehicle params to take care of all the vehicles
vehicles = CustomVehicleParams()

# add human drivers with premade controllers/routers
vehicles.add("human",
             acceleration_controller=(IDMController, {}),
             routing_controller=(GridRouter, {}),
             num_vehicles=Params.human_vehicle_num)

# add RL agents with premade controller
# add coop agents
vehicles.add(
    "RL_coop",
    acceleration_controller=(RLController, {}),
    routing_controller=(GridRouter, {}),
    num_vehicles=Params.coop_rl_vehicle_num,
    cooperative_weight=Params.coop_weight
)

# add selfish agent
vehicles.add(
    "RL_selfish",
    acceleration_controller=(RLController, {}),
    routing_controller=(GridRouter, {}),
    num_vehicles=Params.selfish_rl_vehicle_num,
    cooperative_weight=0
)


########################
#       ENV PARAM
########################

additional_env_params = deepcopy(ADDITIONAL_ENV_PARAMS)
# the reward parameters for the acceleration


# initializing env params, since env is just Test there will be no learning, but the procedure is the same
env_params = EnvParams(additional_params=additional_env_params, horizon=Params.HORIZON, sims_per_step=5, )


#######################
# SUMO + INITIAL CONFIG
########################


# the simulation parameters
sim_params = SumoParams(
    render=True,
    show_radius=True,  # show a circle on top of RL agents
    overtake_right=True,  # overtake on right to simulate more aggressive behavior
    emission_path=Params.DATA_DIR,
    restart_instance=True,
)

# setting initial configuration files
initial_config = InitialConfig(
    shuffle=True,
    perturbation=50.0,
)

#######################
#       INFLOW
########################

# Adding inflows
inflow= InFlows()

human_inflow= dict(
                veh_type="human",
                probability=Params.inflow_prob_human,
                depart_lane="random",
                depart_speed="random",
                begin=5,  # time in seconds to start the inflow
)

# adding human inflows
inflow_random_edges(inflow, **human_inflow)

#######################
#  NETWORK
########################


# specify net params
net_params = NetParams(
    additional_params=additional_net_params,
    inflows=inflow,
    osm_path=Params.MAP_DIRS_DICT["rome"] + "/osm_bbox.osm.xml"

)


########################
#       GENERAL PARAM
########################

# defining a general dictionary containing every configuration ,
# this will be passed to the gym to make the trainable environment
params = dict(
    # name of the experiment
    exp_tag="simulationRL",

    # name of the flow environment the experiment is running on
    env_name="CustoMultiRL",

    # name of the network class the experiment is running on
    network="OSMap",

    # inflow for network
    vehicles=vehicles,

    # simulator that is used by the experiment
    simulator='traci',

    # sumo-related parameters (see flow.core.params.SumoParams)
    sim=SumoParams(
        render=False,  # no renderer will be displayed for training, this is for speed up
        restart_instance=True, # for performance reasons
        emission_path=Params.emission_path_dir,
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
    initial=initial_config,
)



########################
#  ENV CREATION
########################

# define new trainable enviroment
create_env, gym_name = make_create_env(params=params, version=0)

# get default config for ppo
ppo_config = ppo_default_config( params)

# Register as rllib env
register_env(gym_name, create_env)

########################
#  START OF TRAINING
########################
ray.init(num_cpus=Params.N_CPUS,
         num_gpus=Params.N_GPUS,
         local_mode=Params.DEBUG,  # use local mode when debugging, remove it for performance increase
         )

# defining dictionary for the experiment
experiment_params = dict(

    run="PPO",  # must be the same as the default config
    env=gym_name,
    config={**ppo_config},
    checkpoint_freq=Params.checkpoint_freq,
    checkpoint_at_end=True,
    max_failures=999,
    stop=Params.stop_conditions,
    local_dir=Params.ray_results_dir,

)
# weird thing the function wats
experiment_params = {params["exp_tag"]: experiment_params}

# running the experiment
trials = run_experiments(experiment_params)
