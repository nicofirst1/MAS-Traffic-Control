import os


def join_paths(path1, path2):

    return os.path.join(path1,path2)


class Params:


    ##########################
    #       Path params
    ##########################

    WORKING_DIR=join_paths(os.getcwd().split("FlowMas")[0], "FlowMas")

    MAP_DIRS = dict(

        lust=os.path.join(os.getcwd().split("FlowMas")[0], "FlowMas/maps/LuSTScenario"),
        monaco=os.path.join(os.getcwd().split("FlowMas")[0], "FlowMas/maps/MoSTScenario"),
    )

    DATA_DIR= join_paths(WORKING_DIR,"data")

    ##########################
    # Performance stuff
    ##########################
    N_CPUS = 2
    # number of rollouts per training iteration
    N_ROLLOUTS = 1



    def __init__(self):
        print("Params class initialized")




