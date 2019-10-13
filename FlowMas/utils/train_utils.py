import json

from ray.rllib.agents.registry import get_agent_class

from FlowMas.utils.evaluation import configure_callbacks
from FlowMas.utils.parameters import Params
from flow.utils.rllib import FlowParamsEncoder


def performance_config(config):
    """

    :param config:
    :return:

    # Set the ray.rllib.* log level for the agent process and its workers.
    # Should be one of DEBUG, INFO, WARN, or ERROR. The DEBUG level will also
    # periodically print out summaries of relevant internal dataflow (this is
    # also printed out once at startup at the INFO level).
    "log_level": "INFO",

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

    config["num_workers"] = Params.n_workers
    config["num_gpus"] = Params.n_gpus
    # config["num_cpus_per_worker"]=min(Params.N_CPUS//Params.N_WORKERS,1)
    # config["num_gpus_per_worker"]=Params.N_GPUS
    # config["num_cpus_for_driver"]=Params.N_CPUS
    config["log_level"] = "WARNING"

    return config


def eval_config(config):
    """
    Setting evaluation specific configuration, independent from model chosen

    :type config: object
    :param config: a config dict
    :return:  updated config dict

    Check this https://ray.readthedocs.io/en/latest/rllib-training.html#specifying-parameters

    # Callbacks that will be run during various phases of training. These all
    # take a single "info" dict as an argument. For episode callbacks, custom
    # metrics can be attached to the episode by updating the episode object's
    # custom metrics dict (see examples/custom_metrics_and_callbacks.py). You
    # may also mutate the passed in batch data in your callback.
    "callbacks": {
        "on_episode_start": None,     # arg: {"env": .., "episode": ...}
        "on_episode_step": None,      # arg: {"env": .., "episode": ...}
        "on_episode_end": None,       # arg: {"env": .., "episode": ...}
        "on_sample_end": None,        # arg: {"samples": .., "worker": ...}
        "on_train_result": None,      # arg: {"trainer": ..., "result": ...}
        "on_postprocess_traj": None,  # arg: {
                                      #   "agent_id": ..., "episode": ...,
                                      #   "pre_batch": (before processing),
                                      #   "post_batch": (after processing),
                                      #   "all_pre_batches": (other agent ids),
                                      # }

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

    config = configure_callbacks(config)

    return config


def env_config(config):
    """
    Setting environment specific configuration, independent from model chosen
    :param config: a config dict
    :return:  updated config dict




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

    config["train_batch_size"] = Params.horizon  # batch size
    config["gamma"] = Params.discount_rate  # discount rate
    config["horizon"] = Params.horizon  # rollout horizon
    config["lr"] = Params.learning_rate  # fixme: giving weird problem

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

     # If true, use the Generalized Advantage Estimator (GAE)
    # with a value function, see https://arxiv.org/pdf/1506.02438.pdf.
    "use_gae": True,
    # GAE(lambda) parameter
    "lambda": 1.0,
    # Initial coefficient for KL divergence
    "kl_coeff": 0.2,
    # Size of batches collected from each worker
    "sample_batch_size": 200,
    # Number of timesteps collected for each SGD round
    "train_batch_size": 4000,
    # Total SGD batch size across all devices for SGD
    "sgd_minibatch_size": 128,
    # Whether to shuffle sequences in the batch when training (recommended)
    "shuffle_sequences": True,
    # Number of SGD iterations in each outer loop
    "num_sgd_iter": 30,
    # Stepsize of SGD
    "lr": 5e-5,
    # Learning rate schedule
    "lr_schedule": None,
    # Share layers for value function. If you set this to True, it's important
    # to tune vf_loss_coeff.
    "vf_share_layers": False,
    # Coefficient of the value function loss. It's important to tune this if
    # you set vf_share_layers: True
    "vf_loss_coeff": 1.0,
    # Coefficient of the entropy regularizer
    "entropy_coeff": 0.0,
    # Decay schedule for the entropy regularizer
    "entropy_coeff_schedule": None,
    # PPO clip parameter
    "clip_param": 0.3,
    # Clip param for the value function. Note that this is sensitive to the
    # scale of the rewards. If your expected V is large, increase this.
    "vf_clip_param": 10.0,
    # If specified, clip the global norm of gradients by this amount
    "grad_clip": None,
    # Target value for KL divergence
    "kl_target": 0.01,
    # Whether to rollout "complete_episodes" or "truncate_episodes"
    "batch_mode": "truncate_episodes",
    # Which observation filter to apply to the observation
    "observation_filter": "NoFilter",
    # Uses the sync samples optimizer instead of the multi-gpu one. This does
    # not support minibatches.
    "simple_optimizer": False,

    """

    config["use_gae"] = True  # using generalized advantage estimation
    config["lambda"] = 0.97
    config["sample_batch_size"] = 200
    config["sgd_minibatch_size"] = min(16 * 1024, config["train_batch_size"])  # stochastic gradient descent
    config["kl_target"] = 0.02  # target KL divergence
    config["num_sgd_iter"] = 10  # number of SGD iterations
    config["batch_mode"] = "complete_episodes"

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
    config["train_batch_size"] = Params.horizon

    # Number of steps max to keep in the batch replay buffer
    config["replay_buffer_size"] = 100000

    return config


def maddpg_config(config, env):
    """
    Return a dict representing the config file of a standard MARWIL algorithm in rrlib

    :return:(dict)

    # === Settings for each individual policy ===
    # ID of the agent controlled by this policy
    "agent_id": None,
    # Use a local critic for this policy.
    "use_local_critic": False,

    # === Evaluation ===
    # Evaluation interval
    "evaluation_interval": None,
    # Number of episodes to run per evaluation period.
    "evaluation_num_episodes": 10,

    # === Model ===
    # Apply a state preprocessor with spec given by the "model" config option
    # (like other RL algorithms). This is mostly useful if you have a weird
    # observation shape, like an image. Disabled by default.
    "use_state_preprocessor": False,
    # Postprocess the policy network model output with these hidden layers. If
    # use_state_preprocessor is False, then these will be the *only* hidden
    # layers in the network.
    "actor_hiddens": [64, 64],
    # Hidden layers activation of the postprocessing stage of the policy
    # network
    "actor_hidden_activation": "relu",
    # Postprocess the critic network model output with these hidden layers;
    # again, if use_state_preprocessor is True, then the state will be
    # preprocessed by the model specified with the "model" config option first.
    "critic_hiddens": [64, 64],
    # Hidden layers activation of the postprocessing state of the critic.
    "critic_hidden_activation": "relu",
    # N-step Q learning
    "n_step": 1,
    # Algorithm for good policies
    "good_policy": "maddpg",
    # Algorithm for adversary policies
    "adv_policy": "maddpg",

    # === Optimization ===
    # Learning rate for the critic (Q-function) optimizer.
    "critic_lr": 1e-2,
    # Learning rate for the actor (policy) optimizer.
    "actor_lr": 1e-2,
    # Update the target network every `target_network_update_freq` steps.
    "target_network_update_freq": 0,
    # Update the target by \tau * policy + (1-\tau) * target_policy
    "tau": 0.01,
    # Weights for feature regularization for the actor
    "actor_feature_reg": 0.001,
    # If not None, clip gradients during optimization at this value
    "grad_norm_clipping": 0.5,
    # How many steps of the model to sample before learning starts.
    "learning_starts": 1024 * 25,
    # Update the replay buffer with this many samples at once. Note that this
    # setting applies per-worker if num_workers > 1.
    "sample_batch_size": 100,
    # Size of a batched sampled from replay buffer for training. Note that
    # if async_updates is set, then each worker returns gradients for a
    # batch of this size.
    "train_batch_size": 1024,
    # Number of env steps to optimize for before returning
    "timesteps_per_iteration": 0,



    """

    # todo: split for selfhish and coop agents
    policies = {
        "coop": (None, env.observation_space_dict,
                 env.action_space_dict, {
                     "agent_id": 0,
                     "use_local_critic": "maddpg",
                 }),
        "self": (None, env.observation_space_dict,
                 env.action_space_dict, {
                     "agent_id": 1,
                     "use_local_critic": "dpg",
                 }),
    }

    def mapping(agent):
        if "coop" in agent:
            return  "coop"

        else:
            return "self"

    # config['agent_id']=1
    config['multiagent'] = {
        "policies": policies,
        "policy_mapping_fn": mapping
    }

    return config


def get_default_config(params, env):
    """
    Return the default configuration for a specific type of algorithm
    :param params: (dict)  general dictionary containing every configuration parameter (env, netwrok, inflow ...)
    :return:(dict)
    """

    # get original config from alg
    config = get_agent_class(Params.training_alg)._default_config.copy()

    # apply alg-free changes
    config = env_config(config)
    config = eval_config(config)
    config = model_config(config)
    config = flow_config(params, config)
    config = performance_config(config)

    if Params.training_alg == "PPO":
        config = ppo_config(config)

    elif Params.training_alg == "MARWIL":
        config = marwil_config(config)


    elif Params.training_alg == "contrib/MADDPG":
        config = maddpg_config(config, env)

    else:
        raise NotImplementedError(f"{Params.training_alg} has not been implemented")

    return config
