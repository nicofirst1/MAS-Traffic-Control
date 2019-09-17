import os

import ray

from FlowMas.utils import ppo_default_config, N_CPUS
# the Experiment class is used for running simulations
from flow.controllers import RLController, ContinuousRouter
from flow.core.params import EnvParams
from flow.core.params import NetParams
from flow.core.params import SumoParams
# all other imports are standard
from flow.core.params import VehicleParams
# the base network class
from flow.networks.traffic_light_grid import ADDITIONAL_NET_PARAMS
from maps_utils import import_map

try:
    from ray.rllib.agents.agent import get_agent_class
except ImportError:
    from ray.rllib.agents.registry import get_agent_class
from ray.tune import run_experiments
from ray.tune.registry import register_env

from flow.utils.registry import make_create_env

# Define horizon as a variable to ensure consistent use across notebook
HORIZON = 100

# get the LUST dir
LuST_dir = os.path.join(os.getcwd().split("FlowMas")[0], "FlowMas/data/maps/LuSTScenario")

# Remove traffic lights
ADDITIONAL_NET_PARAMS['traffic_lights'] = False

# specify net params
net_params = NetParams(
    template=import_map("lust", net=True, vtype=True, rou=True),
    additional_params=ADDITIONAL_NET_PARAMS,

)

# we no longer need to specify any humans  in VehicleParams
vehicles = VehicleParams()

# adding rl agents
vehicles.add(veh_id="rl",
             acceleration_controller=(RLController, {}),
             routing_controller=(ContinuousRouter, {}),
             num_vehicles=1)

# create some default parameters parameters
env_params = EnvParams(
    # length of one rollout
    horizon=HORIZON,

    additional_params={
        # maximum acceleration of autonomous vehicles
        "max_accel": 1,
        # maximum deceleration of autonomous vehicles
        "max_decel": 1,
    },
)

# Creating flow_params. Make sure the dictionary keys are as specified.
flow_params = dict(
    # name of the experiment
    exp_tag="training_example",
    # name of the flow environment the experiment is running on
    env_name="TestEnv",  # can be found in envs.__init__.py
    # name of the network class the experiment uses
    network="LuSTNetwork",
    # simulator that is used by the experiment
    simulator='traci',
    # sumo-related parameters (see flow.core.params.SumoParams)
    sim=SumoParams(sim_step=0.1, render=False),
    # environment related parameters (see flow.core.params.EnvParams)
    env=env_params,
    # network-related parameters (see flow.core.params.NetParams and
    # the network's documentation or ADDITIONAL_NET_PARAMS component)
    net=net_params,
    # vehicles to be placed in the network at the start of a rollout
    # (see flow.core.vehicles.Vehicles)
    veh=vehicles,

)

# Call the utility function make_create_env to be able to
# register the Flow env for this experiment
create_env, gym_name = make_create_env(params=flow_params, version=0)

# Register as rllib env with Gym
register_env(gym_name, create_env)

ray.init(redirect_output=True, num_cpus=N_CPUS)

# get the default config for ppo algorithm
config = ppo_default_config(HORIZON, flow_params)

trials = run_experiments({
    flow_params["exp_tag"]: {
        "run": "PPO",
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
