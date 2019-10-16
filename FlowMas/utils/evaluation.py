import itertools
import json
import logging
import os
from collections import Counter

import numpy as np
import termcolor
# avaiable colors : red, green, yellow, blue, magenta, cyan, white.
from ray.tune.logger import JsonLogger
from tabulate import tabulate

from FlowMas.utils.parameters import Params

step_color = "cyan"
start_color = "green"
end_color = "green"
train_color = "yellow"
logger = logging.getLogger("ray")


class CustomJsonLogger(JsonLogger):
    """
    Overload of json logger used to discard long env configuration during the result logging,
    it also saves the custom Params class at the start
    """

    def _init(self):
        # save parameter class
        params_out = os.path.join(self.logdir, "parameter_attributes.json")
        with open(params_out, "w") as f:
            json.dump(
                Params.get_attributes__(Params),
                f,
                indent=4,
                sort_keys=True, )

        super()._init()

    def on_result(self, result):
        """
        Override method to remove config from result
        :param result:
        :return:
        """
        result['config'] = {}
        super().on_result(result)


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
       Extract information regarding the delays
       :param info: dict, containing the general information given by the callback
       :return: dict, delays values for each agent as well as the total one
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

    delay = {k: np.mean(v) for k, v in delay.items()}
    return delay


def get_reward_info(info):
    """
       Extract information regarding the rewards
       :param info: dict, containing the general information given by the callback
       :return: dict, rewards values for each agent as well as the total one
       """

    # get the episode from the infos
    info = info.get("episode")
    # convert history to normal dict
    reward_history = dict(info._agent_reward_history)
    rewards = dict(all=[])

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
        rewards["all"] += v

    # convert to numpy array
    rewards = {k: np.mean(v) for k, v in rewards.items()}

    return rewards


def get_action_info(info):
    """
       Extract information regarding the actions
       :param info: dict, containing the general information given by the callback
       :return: dict, actions values for each agent as well as the total one
       """

    # get the episode from the infos
    info = info.get("episode")._agent_to_last_action

    # return if zero length
    if len(info) == 0:
        return []

    actions = dict(all=[])

    # for every id:list in the history of rewards
    for k, v in info.items():
        # split the name to get the type of agent
        new_k = k.rsplit("_", 1)[0]

        if new_k not in actions.keys():
            actions[new_k] = []

        # add history to list
        actions[new_k].append(v)
        actions["all"].append(v)

        # convert to numpy array
    actions = {k: np.mean(v) for k, v in actions.items()}

    return actions


def get_jerk_info(info):
    """
    Extract information regarding the jerk
    :param info: dict, containing the general information given by the callback
    :return: dict, jerk values for each agent as well as the total one
    """
    env = info['env'].envs[0]

    ids = env.k.vehicle.get_rl_ids()
    ids = {k: env.k.vehicle.get_jerk(k) for k in ids}

    jerks = dict(all=[])

    for ag, jrk in ids.items():
        ag = ag.rsplit('_', 1)[0]

        if ag not in jerks.keys():
            jerks[ag] = []

        jerks[ag].append(jrk)
        jerks["all"].append(jrk)

    jerks = {k: np.mean(v) for k, v in jerks.items()}
    return jerks


def get_env_infos(info):
    """
    Extract information regarding the environment
    :param info: dict, containing the general information given by the callback
    :return: str, printable info
    """
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
    msg = termcolor.colored(msg, color)
    print_title(msg)
    logger.info(msg)


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
    Custom callback to be called
    :param info:
    :return:
    """
    # todo: get action min/max/mean

    # get reward infos
    rewards = get_reward_info(info)
    delays = get_delay_info(info)
    jerks = get_jerk_info(info)
    actions = get_action_info(info)

    msg = ""

    if len(rewards) != 0:
        if Params.verbose >= 3:
            msg += dict_print(rewards, "Rewards")
        info["episode"].user_data["rewards"].append(rewards)

    if len(delays) != 0:
        if Params.verbose >= 3:
            msg += dict_print(delays, "Delays")

        info["episode"].user_data["delays"].append(delays)

    if len(jerks) != 0:
        if Params.verbose >= 3:
            msg += dict_print(jerks, "Jerks")

        info["episode"].user_data["jerks"].append(jerks)

    if len(actions) != 0:
        if Params.verbose >= 3:
            msg += dict_print(actions, "Actions")

        info["episode"].user_data["actions"].append(actions)

    if Params.verbose >= 3:
        log(msg, color=step_color)


def on_episode_start(info):
    """
    Custom callback to be run on the start of an episode, logs some env params
    :param info: dict, information about run
    :return: None
    """
    msg = print_title("EPISODE STARTED", hash_num=60)
    msg += get_env_infos(info)

    # Initialize lists for user data to be used later on
    info["episode"].user_data["rewards"] = []
    info["episode"].user_data["delays"] = []
    info["episode"].user_data["actions"] = []
    info["episode"].user_data["jerks"] = []

    log(msg, color=start_color)


def on_episode_end(info):
    """
    Custom callback to be called when an episode ends
    :param info: dictionary containing all the information
    :return:
    """

    def chain_list(dict_list):
        """
        Flat dictionary to make it printalbe
        :param dict_list:
        :return:
        """

        tmp = {k: [] for k in dict_list[0].keys()}
        for elem in dict_list:
            for k, v in elem.items():
                tmp[k].append(v)

        return tmp

    def add_to_metrics(what, metrics, name):
        """
        Add information to metric
        :param what: dictionary of infos§
        :param metrics: dict to be updated
        :param name: str, name of the updated value
        :return: None
        """

        for k, v in what.items():
            new_k = "/".join((name, k))

            metrics.update(
                {new_k: v}
            )

    episode = info["episode"]
    # add end episode to message§
    msg = print_title("EPISODE END", hash_num=60)

    # get every custom metric list from the userd data field
    delays = episode.user_data["delays"]
    rewards = episode.user_data["rewards"]
    jerks = episode.user_data["jerks"]
    actions = episode.user_data["actions"]

    # flat the list
    delays = chain_list(delays)
    rewards = chain_list(rewards)
    jerks = chain_list(jerks)
    actions = chain_list(actions)

    # get the mean for every episode
    jerks = {k: np.mean(v) for k, v in jerks.items()}
    delays = {k: np.mean(v) for k, v in delays.items()}
    rewards = {k: np.mean(v) for k, v in rewards.items()}
    actions = {k: np.mean(v) for k, v in actions.items()}

    custom = episode.custom_metrics
    # add to custom metrics
    add_to_metrics(delays, custom, "Delays")
    add_to_metrics(rewards, custom, "Rewards")
    add_to_metrics(jerks, custom, "Jerks")
    add_to_metrics(actions, custom, "Actions")

    # update custom metrics
    episode.custom_metrics = custom

    # log message
    log(msg, color=end_color)


def on_train_result(info):
    """
    Custom callback to be called on the end of a trainig instance
    :param info: dict, usefull infos about the training result
    :return: None
    """

    result = info["result"]

    policy_reward_mean = {}
    for ag, jrk in result["policy_reward_mean"].items():
        ag = ag.rsplit('_', 1)[0]

        if ag not in policy_reward_mean.keys():
            policy_reward_mean[ag] = []

        policy_reward_mean[ag].append(jrk)
        policy_reward_mean["all"].append(jrk)

    policy_reward_mean = {k: np.mean(v) for k, v in policy_reward_mean.items()}

    table = dict(

        episodes_total=result["episodes_total"],
        training_iteration=result["training_iteration"],
        time_this_iter_s=result["time_this_iter_s"],
        time_total_s=result["time_total_s"],
        timesteps_total=result["timesteps_total"],
        policy=json.dumps(policy_reward_mean, indent=4),
        perf=json.dumps(result["perf"], indent=4),
        episode_reward_mean=result["episode_reward_mean"],
        episode_len_mean=result["episode_len_mean"],
    )

    msg = "\n"
    msg += tabulate(list(table.items()), tablefmt="grid")
    log(msg, train_color)
