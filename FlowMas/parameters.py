import os


def join_paths(path1, path2):

    return os.path.join(path1,path2)


class Params:


    ##########################
    #       Path params
    ##########################

    WORKING_DIR=join_paths(os.getcwd().split("FlowMas")[0], "FlowMas")

    MAP_DIRS = dict(

        lust=join_paths(WORKING_DIR, "maps/LuSTScenario"),
        monaco=join_paths(WORKING_DIR, "maps/MoSTScenario"),
        rome= join_paths(WORKING_DIR, "maps/RomeOSM")
    )

    DATA_DIR= join_paths(WORKING_DIR,"data")

    ##########################
    # Performance stuff
    ##########################
    N_CPUS = 2
    # number of rollouts per training iteration
    N_ROLLOUTS = 1


    ##########################
    # Scenarios and Network
    ##########################

    map="rome"
    percentage_edges=0.3

    def __init__(self):
        print("Params class initialized")




