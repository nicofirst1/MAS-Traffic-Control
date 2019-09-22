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
        groningen = join_paths(WORKING_DIR, "maps/GroningenOSM"),
    )

    DATA_DIR = join_paths(WORKING_DIR, "data")

    ##########################
    # Agent  params
    ##########################
    # todo: make distance dependent of map measures
    min_neighbors_distance = 50  # minunum distance between vehicle to be considered neighbors (in meters)

    ##########################
    # Performance stuff
    ##########################
    N_CPUS = 4
    # number of rollouts per training iteration
    N_ROLLOUTS = 1

    DEBUG=False

    ##########################
    # Scenarios and Network
    ##########################

    map = "rome"
    percentage_edges = 0.3

    def __init__(self):
        print("Params class initialized")
