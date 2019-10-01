# number of parallel workers
import json

from ray.rllib.agents.registry import get_agent_class

from FlowMas.utils.parameters import Params
from flow.utils.rllib import FlowParamsEncoder
from FlowMas.utils.maps_utils import get_edges


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

