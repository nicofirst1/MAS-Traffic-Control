import argparse
import inspect
import json
import multiprocessing
import os
import shutil
import sys

import termcolor
from tensorflow.python.client import device_lib


def join_paths(path1, path2):
    return os.path.join(path1, path2)


class Params:
    ##########################
    #       Path params
    ##########################

    WORKING_DIR = join_paths(os.getcwd().split("FlowMas")[0], "FlowMas")

    MAP_DIRS_DICT = dict(

        rome=join_paths(WORKING_DIR, "maps/RomeOSM"),
        groningen=join_paths(WORKING_DIR, "maps/GroningenOSM"),
    )

    DATA_DIR = join_paths(WORKING_DIR, "data")
    emission_path_dir = join_paths(DATA_DIR, "emission_path")
    ray_results_dir = join_paths(DATA_DIR, "ray_results")

    ##########################
    # Performance stuff
    ##########################
    debug = True

    # level of verbosity
    # 0 : print start/end of episode
    # 1 : same as 0 + verbose ray level 1
    # 2 : same as 1 + verbose ray level 2
    # 3 : same as 2 + print at each time step
    # 4 : same as 3 + verbose for sumo
    verbose = 1

    # get max number of cpu available
    n_cpus = multiprocessing.cpu_count() if not debug else 1  # avoiding error 6

    # get number og tensorflow recognizable gpus
    gpus = len([x.name for x in device_lib.list_local_devices() if  'GPU' in x.device_type ])
    n_gpus = gpus if not debug else 0  # avoiding error 6

    # set the number of workers
    n_workers =1

    trial_resources = dict(
        cpu=n_cpus,
        gpu=n_gpus,
    )

    ##########################
    # Agent  params
    ##########################
    # minimum distance between vehicle to be considered neighbors (in meters)
    min_neighbors_distance = 50

    # the duration of one episode in steps.
    horizon = 500 if not debug else 100  # set to 1 for debug in order to start learning immediately

    # the weight for cooperative agents (1-> fully coop, 0-> selfish)
    coop_weight = 1

    # baseline for reward
    baseline = 10

    clip_action=False

    ##########################
    #  Training  params
    ##########################

    # number fo units for model
    num_units = 64

    # frequency of checkpoint
    checkpoint_freq = 5

    evaluation_num_episodes=10 if not debug else 2


    ##############
    # Batches size
    ##############
    # size for learning batch, note that this value will be divided by the number of workers so to have at most
    # 'sample_batch_size' for the entire training
    train_batch_size= horizon//2
    sample_batch_size=train_batch_size//2

    # number of episode after which the training start, and repeats itself
    learning_starts = train_batch_size

    # number of iterations for training
    training_iteration = 600 if not debug else 100
    episode_num = 9999 if not debug else 15

    # training algorithms
    implemented_algs = ["MARWIL", "contrib/MADDPG", "PPO"]  # see journal, research section
    training_alg = implemented_algs[1]

    # learning rate
    learning_rate = 1e-4

    # dictionary for stopping conditions
    stop_conditions = dict(

        training_iteration=training_iteration,
        episodes_total=episode_num,
    )

    discount_rate = 0.998

    ##########################
    # Scenarios and Network
    ##########################

    # the map to be used
    map = "groningen"

    # INFLOW PARAMS

    # percentage of edges to keep for random inflow
    percentage_edges = 0.3

    # probability to spawn a human
    inflow_prob_human = 0.001

    # Number of cols and rows for grid network
    cols=5
    rows=5

    # gap (in meters) for cars in initial starting position
    dx=10

    # number of humans in the initial config
    human_vehicle_num = 300

    # number of selfish/coop rl agents in the initial conf
    selfish_rl_vehicle_num = 20 if not debug else 4
    coop_rl_vehicle_num = 40  if not debug else 8
    num_agents = coop_rl_vehicle_num + selfish_rl_vehicle_num

    # Time for a simulation step
    sim_step=0.1

    ##########################
    #    METHODS
    ##########################

    def __parse_args(self):
        """
        Use argparse to change the default values in the param class
        """

        EXAMPLE_USAGE = "python FlowMas/train.py {args}"

        att = self.get_attributes__()

        """Create the parser to capture CLI arguments."""
        parser = argparse.ArgumentParser(
            formatter_class=argparse.RawDescriptionHelpFormatter,
            description="Starts the trainig for a custom agent",
            epilog=EXAMPLE_USAGE)

        # for every attribute add an arg instance
        for k, v in att.items():
            parser.add_argument(
                "--" + k.lower(), type=type(v), default=v,
            )

        args = parser.parse_args()
        # setting args
        for k, v in vars(args).items():
            self.__setattr__(k, v)

    def __init__(self):
        print("Params class initialized")
        self.__initialize_dirs()

        # change values based on argparse
        self.__parse_args()
        self.__log_params()

    def get_attributes__(self):
        """
        Get a dictionary for every attribute that does not have "filter_str" in it
        :return:
        """

        # get every attribute
        attributes = inspect.getmembers(self)
        # filter based on double underscore
        filter_str = "__"
        attributes = [elem for elem in attributes if filter_str not in elem[0]]
        # convert to dict
        attributes = dict(attributes)

        return attributes

    def __log_params(self, stdout=sys.stdout):
        """
        Prints attributes as key value on given output
        :param stdout: the output for printing, default stdout
        :return:
        """

        # initializing print message
        hashes = f"\n{20 * '#'}\n"
        msg = f"{hashes} PARAMETER START {hashes}"

        # get the attributes ad dict
        attributes = self.get_attributes__()
        # dump using jason
        attributes = json.dumps(attributes, indent=4, sort_keys=True)

        msg += attributes
        msg += f"{hashes} PARAMETER END {hashes}"

        color = "yellow"
        msg = termcolor.colored(msg, color=color)

        # print them to given out
        print(msg, file=stdout)

    def __initialize_dirs(self):
        """
        Initialize all the directories  listed above
        :return:
        """
        variables = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]
        for var in variables:
            if var.lower().endswith('dir'):
                path = getattr(self, var)
                if not os.path.exists(path):
                    termcolor.colored(f"Mkdir {path}", "yellow")
                    os.makedirs(path)

    def __empty_dirs(self, to_empty):
        """
        Empty all the dirs in to_empty
        :return:
        """

        for folder in to_empty:
            try:
                for the_file in os.listdir(folder):
                    file_path = os.path.join(folder, the_file)
                    try:
                        if os.path.isfile(file_path):
                            os.unlink(file_path)
                        elif os.path.isdir(file_path):
                            shutil.rmtree(file_path)
                    except Exception as e:
                        print(e)
            except Exception:
                continue
