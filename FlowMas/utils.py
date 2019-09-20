# number of parallel workers
import json

from ray.rllib.agents.registry import get_agent_class

from FlowMas.parameters import Params
from flow.utils.rllib import FlowParamsEncoder
from maps_utils import get_edges


def inflow_random_edges(inflow, **kwargs):
    """
    Add inflow from random edges.
    :param inflow: the inflow class
    :param map_name: the map name from which to take random edges
    :param perc_edges: the percentage of edges to take from the map
    :param kwargs: a dictionary for the
    inflow class (note that the key 'edges' will be removed and the key 'vehs_per_hour' will be rescaled by the
    number of chosen edges) :return: None
    """

    # get the edges
    edges = get_edges(Params.map, perc=Params.percentage_edges)

    # scale the vehs_per_hour parameter by the number of edges
    if "vehs_per_hour" in kwargs.keys():
        kwargs["vehs_per_hour"] = kwargs["vehs_per_hour"] / len(edges)

    # remove edges key if in kwargs
    if "edge" in kwargs.keys():
        del kwargs['edge']

    # for each edge add an inflow
    for edge in edges:
        inflow.add(
            edge=edge,
            **kwargs,
        )


def ppo_default_config(horizon, params):
    """
    Return a dict representing the config file of a standard PPO algorithm in rrlib

    :param horizon: (int) duration of one episode (during which the RL-agent acquire data).
    :param params: (dict)  general dictionary containing every configuration parameter (env, netwrok, inflow ...)
    :return:(dict)
    
    """
    alg_run = "PPO"

    config = get_agent_class(alg_run)._default_config.copy()
    config["num_workers"] = Params.N_CPUS - 1  # number of parallel workers
    config["train_batch_size"] = horizon * Params.N_ROLLOUTS  # batch size
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
