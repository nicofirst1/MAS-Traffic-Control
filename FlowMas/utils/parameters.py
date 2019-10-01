import os
import shutil

import termcolor


def join_paths(path1, path2):
    return os.path.join(path1, path2)


class Params:
    ##########################
    #       Path params
    ##########################

    WORKING_DIR = join_paths(os.getcwd().split("FlowMas")[0], "FlowMas")

    MAP_DIRS_DICT = dict(

        lust=join_paths(WORKING_DIR, "maps/LuSTScenario"),
        monaco=join_paths(WORKING_DIR, "maps/MoSTScenario"),
        rome=join_paths(WORKING_DIR, "maps/RomeOSM"),
        groningen=join_paths(WORKING_DIR, "maps/GroningenOSM"),
    )

    DATA_DIR = join_paths(WORKING_DIR, "data")
    emission_path_dir = join_paths(DATA_DIR, "emission_path")
    ray_results_dir = join_paths(DATA_DIR, "ray_results")


    ##########################
    # Performance stuff
    ##########################
    DEBUG = True
    N_CPUS = 4 if not DEBUG else 1 # avoiding error 6
    N_GPUS = 0 if not DEBUG else 0 # avoiding error 6

    trial_resources=dict(
        cpu= N_CPUS,
        gpu=N_GPUS,
    )

    ##########################
    # Agent  params
    ##########################
    # todo: make distance dependent of map measures
    # minimum distance between vehicle to be considered neighbors (in meters)
    min_neighbors_distance = 50

    # number of rollouts per training iteration
    N_ROLLOUTS = 1

    # the duration of one episode (during which the RL-agent acquire data).
    HORIZON = 1500 if not DEBUG else 1 # set to 1 for debug in order to start learning immediately

    # the weight for cooperative agents (1-> super coop, 0-> selfish)
    coop_weight = 0.7

    # baseline for reward
    baseline = 10

    ##########################
    #  Training  params
    ##########################

    # Number of evaluation to perform
    evaluation_interval=4

    # frequency of checkpoint
    checkpoint_freq = 20

    #number of iterations for training
    training_iteration = 600

    # training algorithms
    implemented_algs=["MARWIL","PPO"]
    training_alg=implemented_algs[0]

    # learning rate
    learning_rate=1e-4

    # dictionary for stopping conditions
    stop_conditions = dict(

        training_iteration=training_iteration
    )

    discount_rate = 0.998

    ##########################
    # Scenarios and Network
    ##########################

    # the map to be used
    map = "groningen"

    # number of humans in the initial config
    human_vehicle_num = 100

    # number of selfish/coop rl agents in the initial conf
    selfish_rl_vehicle_num = 70
    coop_rl_vehicle_num = 150

    # INFLOW PARAMS

    # percentage of edges to keep for random inflow
    percentage_edges = 0.3

    # probability to spawn a human
    inflow_prob_human = 0.001

    ##########################
    #    METHODS
    ##########################

    def __init__(self):
        print("Params class initialized")
        #self.empty_dirs([self.LOGS_DIR, self.SONG_DIR])
        self.initialize_dirs()

    def initialize_dirs(self):
        """
        Initialize all the directories  listed above
        :return:
        """
        variables = [attr for attr in dir(self) if not callable(getattr(self, attr)) and not attr.startswith("__")]
        for var in variables:
            if var.lower().endswith('dir'):
                path = getattr(self, var)
                if not os.path.exists(path):
                    termcolor.colored(f"Mkdir {path}","yellow")
                    os.makedirs(path)

    def empty_dirs(self, to_empty):
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


Params()