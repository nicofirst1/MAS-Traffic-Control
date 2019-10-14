import itertools
import json
import os
from collections import Counter
from tabulate import tabulate
import cloudpickle
import numpy as np
import termcolor

# avaiable colors : red, green, yellow, blue, magenta, cyan, white.
from ray.tune.logger import  JsonLogger
import logging
from FlowMas.utils.parameters import Params

step_color = "cyan"
start_color = "green"
end_color = "green"
train_color = "yellow"
logger = logging.getLogger("ray")


class CustomoJsonLogger(JsonLogger):

    def _init(self):

        # save parameter

        params_out = os.path.join(self.logdir, "parameter_attributes.json")
        with open(params_out, "w") as f:
            json.dump(
                Params.get_attributes__(Params),
                f,
                indent=4,
                sort_keys=True,)

        super()._init()

    def on_result(self, result):
        """
        Override method to remove config from result
        :param result:
        :return:
        """
        result['config']={}
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


    return infos



def get_jerk_info(info):

    env=info['env'].envs[0]

    ids=env.k.vehicle.get_rl_ids()
    ids={k:env.k.vehicle.get_jerk(k) for k in ids}

    jerks={}

    for ag,jrk in ids.items():
        ag=ag.rsplit('_', 1)[0]

        if ag not in jerks.keys():
            jerks[ag]=[]

        jerks[ag].append(jrk)

    jerks=multi_info_split(jerks, "Jerk")
    return jerks


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
    msg=termcolor.colored(msg,color)
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
    On step function for debugging and traning
    :param info:
    :return:
    """
    # todo: mean jerk (?)
    # todo: get action min/max/mean

    # get reward infos
    rewards = get_reward_info(info)
    delays = get_delay_info(info)
    jerks=get_jerk_info(info)

    msg = ""

    if len(rewards) != 0:
        if Params.verbose >= 3:
            msg += dict_print(rewards, "Rewards")
        info["episode"].user_data["rewards"]["split"].append(rewards[0])
        info["episode"].user_data["rewards"]["total"].append(rewards[1])

    if len(delays) != 0:
        if Params.verbose >= 3:
            msg += dict_print(delays, "Delays")

        info["episode"].user_data["delays"]["split"].append(delays[0])
        info["episode"].user_data["delays"]["total"].append(delays[1])

    if len(jerks) != 0:
        if Params.verbose >= 3:
            msg += dict_print(jerks, "Jerks")

        info["episode"].user_data["jerks"]["split"].append(jerks[0])
        info["episode"].user_data["jerks"]["total"].append(jerks[1])

    if Params.verbose >= 3:
        log(msg, color=step_color)


def on_episode_start(info):
    msg = print_title("EPISODE STARTED", hash_num=60)
    msg += get_env_infos(info)

    info["episode"].user_data["rewards"] = dict(
        total=[],
        split=[],
    )
    info["episode"].user_data["delays"] = dict(
        total=[],
        split=[],
    )

    info["episode"].user_data["jerks"] = dict(
        total=[],
        split=[],
    )

    log(msg, color=start_color)

    # remove env config from dict to avoid heavy files




def outer_split(to_split, name):
    prov = {}

    for elem in to_split:

        for k, v in elem.items():

            if k == "name": continue

            for k2, v2 in v.items():

                new_k = "/".join([name, k, k2])
                if new_k not in prov.keys():
                    prov[new_k] = []

                prov[new_k].append(v2)

    return prov


def inner_split(to_split, title):
    prov = {}

    for elem in to_split:

        for k2, v2 in elem.items():
            if k2 == "name": continue

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
    jerks = episode.user_data["jerks"]

    delay_total = delays['total']
    delay_split = delays['split']

    reward_total = rewards['total']
    reward_split = rewards['split']

    jerk_total = jerks['total']
    jerk_split = jerks['split']

    custom = episode.custom_metrics

    tmp = outer_split(delay_split, "Delays/Split")
    tmp = {k: np.mean(v) for k, v in tmp.items()}
    custom.update(tmp)

    tmp = outer_split(reward_split, "Rewards/Split")
    tmp = {k: np.mean(v) for k, v in tmp.items()}
    custom.update(tmp)

    tmp = outer_split(jerk_split, "Jerk/Split")
    tmp = {k: np.mean(v) for k, v in tmp.items()}
    custom.update(tmp)

    tmp = inner_split(delay_total, "Delays/Total")
    tmp = {k: np.mean(v) for k, v in tmp.items()}
    custom.update(tmp)

    tmp = inner_split(reward_total, "Rewards/Total")
    tmp = {k: np.mean(v) for k, v in tmp.items()}
    custom.update(tmp)

    tmp = inner_split(jerk_total, "Jerk/Total")
    tmp = {k: np.mean(v) for k, v in tmp.items()}
    custom.update(tmp)

    episode.custom_metrics = custom

    log(msg, color=end_color)


def on_train_result(info):

    result=info["result"]

    table=dict(

        episodes_total=result["episodes_total"],
        training_iteration=result["training_iteration"],
        time_this_iter_s=result["time_this_iter_s"],
        time_total_s=result["time_total_s"],
        timesteps_total=result["timesteps_total"],
        policy=json.dumps(result["policy_reward_mean"],indent=4),
        perf=json.dumps(result["perf"], indent=4),
        episode_reward_mean=result["episode_reward_mean"],
        episode_len_mean=result["episode_len_mean"],
    )


    msg=tabulate(list(table.items()), tablefmt="grid")
    log(msg,train_color)
