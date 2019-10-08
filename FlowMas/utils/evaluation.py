from datetime import datetime
import itertools
import json
from collections import Counter
import os

import numpy as np
import termcolor
from ray import tune

# avaiable colors : red, green, yellow, blue, magenta, cyan, white.
from FlowMas.utils.parameters import Params

step_color = "cyan"
start_color = "green"
end_color = "green"
train_color = "yellow"


class Memory:

    def __init__(self):
        self.rewards = []
        self.delays = []
        self.window = 10
        print("Memory class initialized")

    def add_reward(self, reward):
        self.rewards.append(reward)

    def add_delay(self, delay):
        self.delays.append(delay)


mem = Memory()



class CustomStdOut(object):
    def _log_result(self, result):
        if result["training_iteration"] % 50 == 0:
            try:
                print("steps: {}, episodes: {}, mean episode reward: {}, agent episode reward: {}, time: {}".format(
                    result["timesteps_total"],
                    result["episodes_total"],
                    result["episode_reward_mean"],
                    result["policy_reward_mean"],
                    round(result["time_total_s"] - self.cur_time, 3)
                ))
            except:
                pass

            self.cur_time = result["time_total_s"]


def configure_callbacks(config):
    config["callbacks"]["on_episode_step"] = on_episode_step
    config["callbacks"]["on_episode_start"] = on_episode_start
    config["callbacks"]["on_episode_end"] = on_episode_end
    config["callbacks"]["on_train_result"] = on_train_result

    return config


###########################
# INFO GETTING
###########################

def get_delay_info(info):
    """
    Prints info about vehicle delays both split and total
    :param info:
    :return:
    """

    # get agent types
    delay = info["env"].envs[0].k.vehicle.get_rl_types()
    delay = {k: np.array([]) for k in delay}

    # get delays for every type of rl agent
    for t in delay.keys():
        delay[t] = np.concatenate((delay[t], info["env"].envs[0].k.vehicle.get_delay(t)))
    # get delays for every vehicle in the system
    delay["all"] = info["env"].envs[0].k.vehicle.get_delay("all")

    # skip if everything is zero (first iter)
    if not any(list(itertools.chain.from_iterable(delay.values()))):
        return []

    infos = multi_info_split(delay, "Delays")

    mem.add_reward(infos)

    return infos


def get_reward_info(info):
    """
    Prints rewards for step, both split and not.
    :param info:
    :return: (string)
    """

    # get the episode from the infos
    info = info.get("episode")
    # convert history to normal dict
    reward_history = dict(info._agent_reward_history)
    rewards = {}

    # return if zero length
    if len(reward_history) == 0:
        return []

    # for every id:list in the history of rewards
    for k, v in reward_history.items():
        # split the name to get the type of agent
        new_k = k.rsplit("_", 1)[0]

        if new_k not in rewards.keys():
            rewards[new_k] = []

        # add history to list
        rewards[new_k] += v

    # convert to numpy array
    rewards = {k: np.array(v) for k, v in rewards.items()}

    infos = multi_info_split(rewards, "Rewards")

    mem.add_reward(infos)

    return infos


def multi_info_split(info, title):
    # split reward by type of agent
    split_info = {k: dict(
        mean=np.mean(v),
        max=np.max(v),
        min=np.min(v)

    ) for k, v in info.items()}

    # add name to dict
    split_info.update(name=f"Split {title}")

    # concat every list
    total_info = list(itertools.chain.from_iterable(info.values()))
    # do the same as before
    total_info = dict(
        name=f"Total {title}",
        mean=np.mean(total_info),
        max=np.max(total_info),
        min=np.min(total_info)

    )

    return split_info, total_info


def get_env_infos(info):
    info = info.get("env").envs[0]
    msg = ""

    env_params = info.env_params
    msg += "Running env with:\n"
    msg += f"Horizion : {env_params.horizon}\n"
    ap = json.dumps(env_params.additional_params, sort_keys=True, indent=4)
    msg += f"Additional params : {ap}\n"

    initial_ids = info.initial_ids
    initial_ids = [elem.rsplit('_', 1)[0] for elem in initial_ids]
    initial_ids = Counter(initial_ids)
    initial_ids = json.dumps(initial_ids, sort_keys=True, indent=4)

    msg += f"Cars number : {initial_ids}\n"

    return msg


###########################
# PRINT FUNCTIONS
###########################

def print_title(title, hash_num=10):
    """
    Print the title
    :param title: string
    :param hash_num: number of hashs
    :return: string
    """

    hashs = hash_num * "#"
    return f"\n{hashs}\n {title} \n{hashs}\n"


def log(msg, color="white"):
    termcolor.cprint(msg, color)


def dict_print(dicts, title, indent=4):
    """
    Print list of dictionaries
    :param dicts: list of dicts
    :param title: string
    :param indent:
    :return:
    """
    msg = print_title(title + " START")

    for d in dicts:
        # make it printable
        msg += json.dumps(d, indent=indent) + "\n"

    msg += print_title(title + " END")

    return msg


###########################
# TUNE FUNCTIONS
###########################

def on_episode_step(info):
    """
    On step function for debugging and traning
    :param info:
    :return:
    """
    # todo: mean jerk (?)
    # todo: get action min/max/mean

    # get reward infos
    rewards = get_reward_info(info)
    delays = get_delay_info(info)

    msg = ""

    if len(rewards) != 0:
        #msg += dict_print(rewards, "Rewards")
        info["episode"].user_data["rewards"].append(rewards)


    if len(delays) != 0:
        #msg += dict_print(delays, "Delays")
        info["episode"].user_data["delays"].append(delays)

    #log(msg, color=step_color)


def on_episode_start(info):
    msg = print_title("EPISODE STARTED", hash_num=60)
    msg += get_env_infos(info)

    info["episode"].user_data["rewards"] = []
    info["episode"].user_data["delays"] = []

    log(msg, color=start_color)

def outer_split(to_split,name):
    prov={}

    for elem in to_split:

        for k,v in elem.items():

            if k=="name":continue

            for k2,v2 in v.items():

                new_k="/".join([name,k,k2])
                if new_k not in prov.keys():
                    prov[new_k] =[]

                prov[new_k].append(v2)

    return prov

def inner_split(to_split, title):
    prov={}

    for elem in to_split:

        for k2, v2 in elem.items():
            if k2=="name":continue

            new_k = "/".join([title, k2])
            if new_k not in prov.keys():
                prov[new_k] = []

            prov[new_k].append(v2)

    return prov

def on_episode_end(info):


    episode = info["episode"]

    msg = print_title("EPISODE END", hash_num=60)

    delays = episode.user_data["delays"]
    rewards = episode.user_data["rewards"]

    delays_split = [elem[0] for elem in delays]
    delays_total = [elem[1] for elem in delays]

    rewards_split = [elem[0] for elem in rewards]
    rewards_total = [elem[1] for elem in rewards]

    custom =episode.custom_metrics
    tmp=outer_split(delays_split, "Delays/Split")
    tmp={k:np.mean(v) for k,v in tmp.items()}
    custom.update(tmp)

    tmp=outer_split(rewards_split, "Rewards/Split")
    tmp={k:np.mean(v) for k,v in tmp.items()}
    custom.update(tmp)

    tmp=inner_split(delays_total, "Delays/Total")
    tmp={k:np.mean(v) for k,v in tmp.items()}
    custom.update(tmp)

    tmp=inner_split(rewards_total, "Rewards/Total")
    tmp={k:np.mean(v) for k,v in tmp.items()}
    custom.update(tmp)

    episode.custom_metrics=custom




    log(msg, color=end_color)



def on_train_result(info):
    log("trainer.train() result: {} -> {} episodes".format(
        info["trainer"], info["result"]["episodes_this_iter"]))
