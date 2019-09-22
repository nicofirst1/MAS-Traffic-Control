import numpy as np
import termcolor
from FlowMas.utils.parameters import Params


def standard_observation(vehicle_api, rl_id, max_speed, max_length):
    """
    Standard observation for agent
    :param vehicle_api: (flow.core.kernel.network.traci.TraCIKernelNetwork) vehicle api
    :param rl_id: (string) id of current agent
    :param max_speed: (float) max speed of system
    :param max_length: (float) max length of map
    :return: (array) with following
     Each observation is  scaled 0-1

            Observation
            1) agent speed
            2) difference between lead speed and agent
            3) distance from leader
            4) difference between agent speed and follower
            5) distance from follower
    """
    this_speed = vehicle_api.get_speed(rl_id)
    lead_id = vehicle_api.get_leader(rl_id)
    follower = vehicle_api.get_follower(rl_id)

    if lead_id in ["", None]:
        # in case leader is not visible
        lead_speed = max_speed
        lead_head = max_length
    else:
        lead_speed = vehicle_api.get_speed(lead_id)
        lead_head = vehicle_api.get_headway(lead_id)

    if follower in ["", None]:
        # in case follower is not visible
        follow_speed = 0
        follow_head = max_length
    else:
        follow_speed = vehicle_api.get_speed(follower)
        follow_head = vehicle_api.get_headway(follower)

    return np.array([
        this_speed / max_speed,
        (lead_speed - this_speed) / max_speed,
        lead_head / max_length,
        (this_speed - follow_speed) / max_speed,
        follow_head / max_length,
    ])


def neighbors_observation(vehicle_api, rl_id, max_speed, max_accel,sim_step):
    """

    Neighbors related observation for agent
    :param vehicle_api: (flow.core.kernel.network.traci.TraCIKernelNetwork) vehicle api
    :param rl_id: (string) id of current agent
    :param max_speed: (float) max speed of system
    :param max_accel: (float) max acceleration for agents
    :param sim_step: (float) simulation step
    :return: (array) with following
     Each observation should be scaled 0-1

            Observation
            1) number of neighbors
            2) average neighbors speed
            3) average neighbors acceleration
    """

    k = vehicle_api.get_neighbors(rl_id, Params.min_neighbors_distance)
    ids = [k for k in k.keys()]

    mean_speed = 0
    mean_acc = 0

    for id in ids:
        mean_speed += vehicle_api.get_speed(id)
        mean_acc += vehicle_api.get_acceleration(id)

    # resolving when len(ids)==0
    mean_speed= 0 if len(ids)==0 else mean_speed/len(ids)
    mean_acc= 0 if len(ids)==0 else mean_acc/len(ids)

    #scaling
    mean_speed/=max_speed
    mean_acc/=max_accel
    mean_acc*=sim_step

    if mean_speed>1 or mean_acc>1 and Params.DEBUG:
        termcolor.colored(f"Speed/acceleration not scaled!\nSpeed={mean_speed}, Acc={mean_acc}","cyan")

    return np.array([
        len(ids),
        mean_speed,
        mean_acc,

    ])
