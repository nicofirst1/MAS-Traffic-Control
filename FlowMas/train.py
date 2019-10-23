from copy import deepcopy

# the Experiment class is used for running simulations
import ray
from ray.tune import register_env, run
from ray.tune.experiment import Experiment
from ray.tune.logger import DEFAULT_LOGGERS
from ray.tune.schedulers import PopulationBasedTraining

from FlowMas.utils.evaluation import CustomJsonLogger
from FlowMas.utils.maps_utils import inflow_random_edges
from FlowMas.utils.parameters import Params
from FlowMas.utils.train_utils import get_default_config
from flow.controllers import IDMController, RLController
from flow.controllers.routing_controllers import GridRouter
from flow.core.params import EnvParams, InitialConfig, CustomVehicleParams
from flow.core.params import NetParams
from flow.core.params import SumoParams
from flow.envs.multiagent.customRL import ADDITIONAL_ENV_PARAMS, CustoMultiRL
from flow.networks.custom_grid import CustomGrid, ADDITIONAL_NET_PARAMS
from flow.utils.registry import make_create_env

try:
    from ray.rllib.agents.agent import get_agent_class
except ImportError:
    from ray.rllib.agents.registry import get_agent_class
from flow.core.params import InFlows

########################
#      VEHICLES
########################

Params()

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
env_params = EnvParams(additional_params=additional_env_params, horizon=Params.horizon, sims_per_step=5, )

#######################
# SUMO + INITIAL CONFIG
########################


# the simulation parameters
sim_params = SumoParams(
    render=False,
    show_radius=True,  # show a circle on top of RL agents
    overtake_right=True,  # overtake on right to simulate more aggressive behavior
    emission_path=Params.emission_path_dir,
    restart_instance=True,
    sim_step=Params.sim_step,

    # port=8873,
)

# setting initial configuration files
initial_config = InitialConfig(
    shuffle=True,
    spacing="custom",
    perturbation=1,
)


#######################
#  NETWORK
########################

additional_net_params = deepcopy(ADDITIONAL_NET_PARAMS)

# Estimating min length for lanes
# getting total number of veh
min_length=Params.num_agents+Params.human_vehicle_num
# split in 4 (top, bottom, right, left)
min_length//=4
# get the maximum between row and cols, split per number
min_length//=max(Params.cols,Params.rows)
# add one (because of int split)
min_length+=1
# multiply per distance gap
min_length*=Params.dx

max_speed=max(additional_net_params["speed_limit"]["vertical"],additional_net_params["speed_limit"]["horizontal"])
max_possible_distance=max_speed*Params.horizon*Params.sim_step-min_length


additional_net_params["grid_array"]=dict(
    row_num=Params.rows,
    col_num=Params.cols,
    inner_length=200,
    short_length=min_length+max_possible_distance,
    long_length=min_length+max_possible_distance,

)

# defining inflow parameters, see later
additional_net_params["horizontal_lanes"] = 1 #todo: increase if control on lane switch


additional_net_params["traffic_lights"]=False

if Params.verbose >= 4:
    additional_net_params['sumo_warnings'] = True
else:
    additional_net_params['sumo_warnings'] = False

# specify net params
net_params = NetParams(
    additional_params=additional_net_params,

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
    network="CustomGrid",

    # inflow for network
    vehicles=vehicles,

    # simulator that is used by the experiment
    simulator='traci',

    # sumo-related parameters (see flow.core.params.SumoParams)
    sim=sim_params,

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

env = CustoMultiRL(env_params, sim_params, CustomGrid(
    Params.map,
    vehicles,
    net_params,
    initial_config=initial_config,
)
                   )

# get default config for ppo
config = get_default_config(params, env)
config['env'] = gym_name  # add env name to the configs

# Register as rllib env
register_env(gym_name, create_env)

########################
#  START OF TRAINING
########################

# initialize ray with performance params
ray.init(num_cpus=Params.n_cpus,
         num_gpus=Params.n_gpus,
         local_mode=Params.debug,  # use local mode when debugging, remove it for performance increase
         )


loggers=list(DEFAULT_LOGGERS)
loggers[0]=CustomJsonLogger


# initialize experiment
exp = Experiment(
    name=f"Sim-{Params.training_alg}",
    run=Params.training_alg,  # must be the same as the default config
    config=config,
    stop=Params.stop_conditions,
    local_dir=Params.ray_results_dir,
    max_failures=5,
    checkpoint_freq=Params.checkpoint_freq,
    checkpoint_at_end=True,
    loggers=loggers,

)

# defining population scheduler
pbt_scheduler = PopulationBasedTraining(
    time_attr='training_iteration',
    metric='episode_reward_mean',
    mode='max',
    perturbation_interval=Params.training_iteration // 100,  # perturbate a total of N times during the training
    hyperparam_mutations={  # fixme: get correct params
        "lr": [1e-4],
    })


# run the experiment
trials = run(
    exp,
    reuse_actors=True,
    verbose=Params.verbose,
    raise_on_failed_trial=True,  # avoid agent not known error
    return_trials=True,
    # scheduler=pbt_scheduler,

)
