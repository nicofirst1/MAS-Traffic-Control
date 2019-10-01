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


def performance_config(config):
    """

    :param config:
    :return:

    # === Resources ===
    # Number of actors used for parallelism
    "num_workers": 2,
    # Number of GPUs to allocate to the trainer process. Note that not all
    # algorithms can take advantage of trainer GPUs. This can be fractional
    # (e.g., 0.3 GPUs).
    "num_gpus": 0,
    # Number of CPUs to allocate per worker.
    "num_cpus_per_worker": 1,
    # Number of GPUs to allocate per worker. This can be fractional.
    "num_gpus_per_worker": 0,
    # Any custom resources to allocate per worker.
    "custom_resources_per_worker": {},
    # Number of CPUs to allocate for the trainer. Note: this only takes effect
    # when running in Tune.
    "num_cpus_for_driver": 1,

    """

    config["num_workers"]=Params.N_WORKERS
    config["num_gpus"]=Params.N_GPUS
    config["num_cpus_per_worker"]=min(Params.N_CPUS//Params.N_WORKERS,1)
    config["num_gpus_per_worker"]=Params.N_GPUS
    config["num_cpus_for_driver"]=Params.N_CPUS
    config["log_level"] = "WARN"


def eval_config(config):
    """
    Setting evaluation specific configuration, independent from model chosen

    :param config: a config dict
    :return:  updated config dict

      # === Evaluation ===
    # Evaluate with every `evaluation_interval` training iterations.
    # The evaluation stats will be reported under the "evaluation" metric key.
    # Note that evaluation is currently not parallelized, and that for Ape-X
    # metrics are already only reported for the lowest epsilon workers.
    "evaluation_interval": None,
    # Number of episodes to run per evaluation period.
    "evaluation_num_episodes": 10,
    # Extra arguments to pass to evaluation workers.
    # Typical usage is to pass extra args to evaluation env creator
    # and to disable exploration by computing deterministic actions
    "evaluation_config": {},
    """

    return config


def env_config(config):
    """
    Setting environment specific configuration, independent from model chosen
    :param config: a config dict
    :return:  updated config dict

    # Set the ray.rllib.* log level for the agent process and its workers.
    # Should be one of DEBUG, INFO, WARN, or ERROR. The DEBUG level will also
    # periodically print out summaries of relevant internal dataflow (this is
    # also printed out once at startup at the INFO level).
    "log_level": "INFO",


        # === Environment ===
    # Discount factor of the MDP
    "gamma": 0.99,
    # Number of steps after which the episode is forced to terminate. Defaults
    # to `env.spec.max_episode_steps` (if present) for Gym envs.
    "horizon": None,
    # Calculate rewards but don't reset the environment when the horizon is
    # hit. This allows value estimation and RNN state to span across logical
    # episodes denoted by horizon. This only has an effect if horizon != inf.
    "soft_horizon": False,
    # Don't set 'done' at the end of the episode. Note that you still need to
    # set this if soft_horizon=True, unless your env is actually running
    # forever without returning done=True.
    "no_done_at_end": False,
    # Arguments to pass to the env creator
    "env_config": {},
    # Environment name can also be passed via config
    "env": None,
    # Whether to clip rewards prior to experience postprocessing. Setting to
    # None means clip for Atari only.
    "clip_rewards": None,
    # Whether to np.clip() actions to the action space low/high range spec.
    "clip_actions": True,
    # Whether to use rllib or deepmind preprocessors by default
    "preprocessor_pref": "deepmind",
    # The default learning rate
    "lr": 0.0001,

    """

    config["train_batch_size"] = Params.HORIZON   # batch size
    config["gamma"] = Params.discount_rate  # discount rate
    config["horizon"] = Params.HORIZON  # rollout horizon
    # config["rl"] = Params.learning_rate #fixme: giving weird problem

    return config


def flow_config(params, config):
    """
    Add flow to configuration dictionary
    :param params: (dict)  general dictionary containing every configuration parameter (env, netwrok, inflow ...)
    :param config: (dict) configuration dict
    :return:
    """
    # save the flow params for replay
    flow_json = json.dumps(params, cls=FlowParamsEncoder, sort_keys=True,
                           indent=4)  # generating a string version of flow_params
    config['env_config']['flow_params'] = flow_json  # adding the flow_params to config dict
    config['env_config']['run'] = Params.training_alg

    return config


def model_config(config):
    """
    Add model parameters to configuration file
    :param config:
    :return:


    MODEL_DEFAULTS = {
    # === Built-in options ===
    # Filter config. List of [out_channels, kernel, stride] for each filter
    "conv_filters": None,
    # Nonlinearity for built-in convnet
    "conv_activation": "relu",
    # Nonlinearity for fully connected net (tanh, relu)
    "fcnet_activation": "tanh",
    # Number of hidden layers for fully connected net
    "fcnet_hiddens": [256, 256],
    # For control envs, documented in ray.rllib.models.Model
    "free_log_std": False,
    # Whether to skip the final linear layer used to resize the hidden layer
    # outputs to size `num_outputs`. If True, then the last hidden layer
    # should already match num_outputs.
    "no_final_linear": False,
    # Whether layers should be shared for the value function.
    "vf_share_layers": True,

    # == LSTM ==
    # Whether to wrap the model with a LSTM
    "use_lstm": False,
    # Max seq len for training the LSTM, defaults to 20
    "max_seq_len": 20,
    # Size of the LSTM cell
    "lstm_cell_size": 256,
    # Whether to feed a_{t-1}, r_{t-1} to LSTM
    "lstm_use_prev_action_reward": False,
    # When using modelv1 models with a modelv2 algorithm, you may have to
    # define the state shape here (e.g., [256, 256]).
    "state_shape": None,

    # == Atari ==
    # Whether to enable framestack for Atari envs
    "framestack": True,
    # Final resized frame dimension
    "dim": 84,
    # (deprecated) Converts ATARI frame to 1 Channel Grayscale image
    "grayscale": False,
    # (deprecated) Changes frame to range from [-1, 1] if true
    "zero_mean": True,

    # === Options for custom models ===
    # Name of a custom preprocessor to use
    "custom_preprocessor": None,
    # Name of a custom model to use
    "custom_model": None,
    # Name of a custom action distribution to use
    "custom_action_dist": None,
    # Extra options to pass to the custom classes
    "custom_options": {},
}

    """
    config["model"].update({"fcnet_hiddens": [16, 16]})  # size of hidden layers in network

    return config


def ppo_config(config):
    """
    Return a dict representing the config file of a standard PPO algorithm in rrlib

    :return:(dict)

    """

    config["use_gae"] = True  # using generalized advantage estimation
    config["lambda"] = 0.97
    config["sgd_minibatch_size"] = min(16 * 1024, config["train_batch_size"])  # stochastic gradient descent
    config["kl_target"] = 0.02  # target KL divergence
    config["num_sgd_iter"] = 10  # number of SGD iterations

    return config


def marwil_config(config):
    """
    Return a dict representing the config file of a standard MARWIL algorithm in rrlib

    :return:(dict)


    """

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

    return config




def get_default_config(params):
    """
    Return the default configuration for a specific type of algorithm
    :param params: (dict)  general dictionary containing every configuration parameter (env, netwrok, inflow ...)
    :return:(dict)
    """

    # get original config from alg
    config = get_agent_class(Params.training_alg)._default_config.copy()

    # apply alg-free changes
    config = env_config(config)
    config = model_config(config)
    config = flow_config(params, config)

    if Params.training_alg == "PPO":
        config = ppo_config(config)

    elif Params.training_alg == "MARWIL":
        config = marwil_config(config)

    else:
        raise NotImplementedError(f"{Params.training_alg} has not been implemented")

    return config

