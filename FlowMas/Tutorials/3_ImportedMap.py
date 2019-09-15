import os

# the Experiment class is used for running simulations
from flow.controllers import RLController, ContinuousRouter
from flow.core.experiment import Experiment
from flow.core.params import EnvParams, InitialConfig
from flow.core.params import NetParams
from flow.core.params import SumoParams
# all other imports are standard
from flow.core.params import VehicleParams
from flow.envs import TestEnv
# the base network class
from flow.networks import Network
from flow.networks.traffic_light_grid import ADDITIONAL_NET_PARAMS
import flow.envs as flowenvs
import json

import ray

from maps_utils import import_map

try:
    from ray.rllib.agents.agent import get_agent_class
except ImportError:
    from ray.rllib.agents.registry import get_agent_class
from ray.tune import run_experiments
from ray.tune.registry import register_env

from flow.utils.registry import make_create_env
from flow.utils.rllib import FlowParamsEncoder


# Define horizon as a variable to ensure consistent use across notebook
HORIZON=100

# create some default parameters parameters
env_params = EnvParams(
    # length of one rollout
    horizon=HORIZON,

    additional_params={
        # maximum acceleration of autonomous vehicles
        "max_accel": 1,
        # maximum deceleration of autonomous vehicles
        "max_decel": 1,
        # bounds on the ranges of ring road lengths the autonomous vehicle
        # is trained on
        "ring_length": [220, 270],
    },
)

# get the LUST dir
LuST_dir = os.path.join(os.getcwd().split("FlowMas")[0],"FlowMas/data/maps/LuSTScenario")

sim_params = SumoParams(render=True, sim_step=1)

# Remove traffic lights
ADDITIONAL_NET_PARAMS['traffic_lights'] = False

# specify net params
net_params = NetParams(
    template=import_map("lust",net=True,vtype=True,rou=True),
    additional_params=ADDITIONAL_NET_PARAMS,

)

# we no longer need to specify any humans  in VehicleParams
vehicles = VehicleParams()

# adding rl agents
vehicles.add(veh_id="rl",
             acceleration_controller=(RLController, {}),
             routing_controller=(ContinuousRouter, {}),
             num_vehicles=5)

network = Network(
    name="template",
    net_params=net_params,
    vehicles=vehicles,
)

# create the environment
env = TestEnv(
    env_params=env_params,
    sim_params=sim_params,
    network=network
)

# Creating flow_params. Make sure the dictionary keys are as specified.
flow_params = dict(
    # name of the experiment
    exp_tag="training_example",
    # name of the flow environment the experiment is running on
    env_name="TrafficLightGridPOEnv",
    # name of the network class the experiment uses
    network=net_params,
    # simulator that is used by the experiment
    simulator='traci',
    # sumo-related parameters (see flow.core.params.SumoParams)
    sim = SumoParams(sim_step=0.1, render=False),
    # environment related parameters (see flow.core.params.EnvParams)
    env=env_params,
    # network-related parameters (see flow.core.params.NetParams and
    # the network's documentation or ADDITIONAL_NET_PARAMS component)
    net=net_params,
    # vehicles to be placed in the network at the start of a rollout
    # (see flow.core.vehicles.Vehicles)
    veh=vehicles,


)


# number of parallel workers
N_CPUS = 2
# number of rollouts per training iteration
N_ROLLOUTS = 1

# The algorithm or model to train. This may refer to "
#      "the name of a built-on algorithm (e.g. RLLib's DQN "
#      "or PPO), or a user-defined trainable function or "
#      "class registered in the tune registry.")
alg_run = "PPO"

agent_cls = get_agent_class(alg_run)
config = agent_cls._default_config.copy()
config["num_workers"] = N_CPUS - 1  # number of parallel workers
config["train_batch_size"] = HORIZON * N_ROLLOUTS  # batch size
config["gamma"] = 0.999  # discount rate
config["model"].update({"fcnet_hiddens": [16, 16]})  # size of hidden layers in network
config["use_gae"] = True  # using generalized advantage estimation
config["lambda"] = 0.97
config["sgd_minibatch_size"] = min(16 * 1024, config["train_batch_size"])  # stochastic gradient descent
config["kl_target"] = 0.02  # target KL divergence
config["num_sgd_iter"] = 10  # number of SGD iterations
config["horizon"] = HORIZON  # rollout horizon

# save the flow params for replay
flow_json = json.dumps(flow_params, cls=FlowParamsEncoder, sort_keys=True,
                       indent=4)  # generating a string version of flow_params
config['env_config']['flow_params'] = flow_json  # adding the flow_params to config dict
config['env_config']['run'] = alg_run

# Call the utility function make_create_env to be able to
# register the Flow env for this experiment
create_env, gym_name = make_create_env(params=flow_params, version=0)

# Register as rllib env with Gym
register_env(gym_name, create_env)


ray.init(redirect_output=True, num_cpus=N_CPUS)


trials = run_experiments({
    flow_params["exp_tag"]: {
        "run": alg_run,
        "env": gym_name,
        "config": {
            **config
        },
        "checkpoint_freq": 1,  # number of iterations between checkpoints
        "checkpoint_at_end": True,  # generate a checkpoint at the end
        "max_failures": 999,
        "stop": {  # stopping conditions
            "training_iteration": 1,  # number of iterations to stop after
        },
    },
})
