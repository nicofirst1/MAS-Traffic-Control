import os


def join_paths(path1, path2):
    return os.path.join(path1, path2)


class Params:
    ##########################
    #       Path params
    ##########################

    WORKING_DIR = join_paths(os.getcwd().split("FlowMas")[0], "FlowMas")

    MAP_DIRS = dict(

        lust=join_paths(WORKING_DIR, "maps/LuSTScenario"),
        monaco=join_paths(WORKING_DIR, "maps/MoSTScenario"),
        rome=join_paths(WORKING_DIR, "maps/RomeOSM"),
        groningen=join_paths(WORKING_DIR, "maps/GroningenOSM"),
    )

    DATA_DIR = join_paths(WORKING_DIR, "data")

    ##########################
    # Agent  params
    ##########################
    # todo: make distance dependent of map measures
    # minimum distance between vehicle to be considered neighbors (in meters)
    min_neighbors_distance = 50

    # number of rollouts per training iteration
    N_ROLLOUTS = 1

    # the duration of one episode (during which the RL-agent acquire data).
    HORIZON = 1500

    # the weight for cooperative agents (1-> super coop, 0-> selfish)
    coop_weight = 0.7

    ##########################
    #  Training  params
    ##########################

    # frequency of checkpoint
    checkpoint_freq = 20

    # dictionary for stopping conditions
    stop_conditions = dict(

        training_iteration=200
    )
    ##########################
    # Performance stuff
    ##########################

    N_CPUS = 4
    N_GPUS = 0
    DEBUG = False

    ##########################
    # Scenarios and Network
    ##########################

    # the map to be used
    map = "rome"

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

    def __init__(self):
        print("Params class initialized")
