import json
import os

from ray.rllib.agents.registry import get_agent_class
from ray.tune import Analysis, Trainable
import numpy as np
from FlowMas.utils.parameters import Params
from flow.utils.rllib import FlowParamsEncoder


def simple_analyzer():
    analysis = Analysis(Params.ray_results_dir)
    df = analysis.dataframe()

    # Get a dataframe for the max accuracy seen for each trial
    df = analysis.dataframe(metric="mean_accuracy", mode="max")

    # Get a dict mapping {trial logdir -> dataframes} for all trials in the experiment.
    all_dataframes = analysis.trial_dataframes

    print(df)
    print(all_dataframes)


def training_config(config):
    """
    Setting training specific configuration, independent from model chosen
    :param config: a config dict
    :return:  updated config dict
    """

    config["num_workers"] = Params.N_CPUS - 1  # number of parallel workers
    config["train_batch_size"] = Params.HORIZON * Params.N_ROLLOUTS  # batch size
    config["gamma"] = Params.discount_rate  # discount rate
    config["horizon"] = Params.HORIZON  # rollout horizon
    config["rl"] = Params.learning_rate  # rollout horizon


def flow_config(params, config,alg_run ):
    """

    :param params: (dict)  general dictionary containing every configuration parameter (env, netwrok, inflow ...)
    :param config: (dict) configuration dict
    :param alg_run: (string) the type of algorithm
    :return:
    """
    # save the flow params for replay
    flow_json = json.dumps(params, cls=FlowParamsEncoder, sort_keys=True,
                           indent=4)  # generating a string version of flow_params
    config['env_config']['flow_params'] = flow_json  # adding the flow_params to config dict
    config['env_config']['run'] = alg_run

    return config


def ppo_config(params):
    """
    Return a dict representing the config file of a standard PPO algorithm in rrlib

    :param params: (dict)  general dictionary containing every configuration parameter (env, netwrok, inflow ...)
    :return:(dict)

    """
    alg_run = "PPO"

    config = get_agent_class(alg_run)._default_config.copy()
    config = training_config(config)

    config["model"].update({"fcnet_hiddens": [16, 16]})  # size of hidden layers in network
    config["use_gae"] = True  # using generalized advantage estimation
    config["lambda"] = 0.97
    config["sgd_minibatch_size"] = min(16 * 1024, config["train_batch_size"])  # stochastic gradient descent
    config["kl_target"] = 0.02  # target KL divergence
    config["num_sgd_iter"] = 10  # number of SGD iterations

    config = flow_config(params, config, alg_run)

    return config


def marwil_config(params):
    """
    Return a dict representing the config file of a standard MARWIL algorithm in rrlib

    :param params: (dict)  general dictionary containing every configuration parameter (env, netwrok, inflow ...)
    :return:(dict)


    """
    alg_run = "MARWIL"

    config = get_agent_class(alg_run)._default_config.copy()
    config = training_config(config)

    # fixme: find good model
    config["model"].update({"fcnet_hiddens": [16, 16]})  # size of hidden layers in network

    # When beta is 0, MARWIL is reduced to imitation learning
    config["beta"] = 1
    # Balancing value estimation loss and policy optimization loss
    config["vf_coeff"] = 1
    # Whether to calculate cumulative rewards
    config["postprocess_inputs"] = True
    # Whether to rollout "complete_episodes" or "truncate_episodes"
    config["batch_mode"] = "complete_episodes"

    # Number of timesteps collected for each SGD round
    config["train_batch_size"] = 2000

    # Number of steps max to keep in the batch replay buffer
    config["replay_buffer_size"] = 100000

    config = flow_config(params, config, alg_run)

    return config


def get_default_config(params):
    """
    Return the default configuration for a specific type of algorithm
    :param params: (dict)  general dictionary containing every configuration parameter (env, netwrok, inflow ...)
    :return:(dict)
    """


    if Params.training_alg=="ppo":
        config=ppo_config(params)

    elif Params.training_alg=="marwil":
        config=marwil_config(params)

    else:
        raise NotImplementedError(f"{Params.training_alg} has not been implemented")

    return config






class MyTrainableClass(Trainable):
    """Example agent whose learning curve is a random sigmoid.
    The dummy hyperparameters "width" and "height" determine the slope and
    maximum reward value reached.
    """

    def _setup(self, config):
        self.timestep = 0

    def _train(self):
        self.timestep += 1
        v = np.tanh(float(self.timestep) / self.config.get("width", 1))
        v *= self.config.get("height", 1)

        # Here we use `episode_reward_mean`, but you can also report other
        # objectives such as loss or accuracy.
        return {"episode_reward_mean": v}

    def _save(self, checkpoint_dir):
        path = os.path.join(checkpoint_dir, "checkpoint")
        with open(path, "w") as f:
            f.write(json.dumps({"timestep": self.timestep}))
        return path

    def _restore(self, checkpoint_path):
        with open(checkpoint_path) as f:
            self.timestep = json.loads(f.read())["timestep"]