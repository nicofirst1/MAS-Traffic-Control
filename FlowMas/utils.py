# number of parallel workers
import json

from flow.utils.rllib import FlowParamsEncoder
from ray.rllib.agents.registry import get_agent_class

N_CPUS = 2
# number of rollouts per training iteration
N_ROLLOUTS = 1


def ppo_default_config(horizon, params):
    """
    Return a dict representing the config file of a standard PPO algorithm in rrlib

    :param horizon: (int) duration of one episode (during which the RL-agent acquire data).
    :param params: (dict)  general dictionary containing every configuration parameter (env, netwrok, inflow ...)
    :return:(dict)
    
    """
    alg_run = "PPO"

    config = get_agent_class(alg_run)._default_config.copy()
    config["num_workers"] = N_CPUS - 1  # number of parallel workers
    config["train_batch_size"] = horizon * N_ROLLOUTS  # batch size
    config["gamma"] = 0.999  # discount rate
    config["model"].update({"fcnet_hiddens": [16, 16]})  # size of hidden layers in network
    config["use_gae"] = True  # using generalized advantage estimation
    config["lambda"] = 0.97
    config["sgd_minibatch_size"] = min(16 * 1024, config["train_batch_size"])  # stochastic gradient descent
    config["kl_target"] = 0.02  # target KL divergence
    config["num_sgd_iter"] = 10  # number of SGD iterations
    config["horizon"] = horizon  # rollout horizon

    # save the flow params for replay
    flow_json = json.dumps(params, cls=FlowParamsEncoder, sort_keys=True,
                           indent=4)  # generating a string version of flow_params
    config['env_config']['flow_params'] = flow_json  # adding the flow_params to config dict
    config['env_config']['run'] = alg_run

    return config
