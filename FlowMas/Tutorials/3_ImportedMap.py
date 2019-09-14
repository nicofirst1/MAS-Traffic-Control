import os

# the Experiment class is used for running simulations
from flow.core.experiment import Experiment
from flow.core.params import EnvParams
from flow.core.params import NetParams
from flow.core.params import SumoParams
# all other imports are standard
from flow.core.params import VehicleParams
from flow.envs import TestEnv
# the base network class
from flow.networks import Network
from flow.networks.traffic_light_grid import ADDITIONAL_NET_PARAMS

# create some default parameters parameters
env_params = EnvParams()

# get the LUST dir
LuST_dir = os.path.join(os.getcwd().split("FlowMas")[0],"FlowMas/data/maps/LuSTScenario")

sim_params = SumoParams(render=True, sim_step=1)

# Remove traffic lights
ADDITIONAL_NET_PARAMS['traffic_lights'] = False

# specify net params
net_params = NetParams(
    template={
        # network geometry features
        "net": os.path.join(LuST_dir, "scenario/lust.net.xml"),
        # features associated with the properties of drivers
        "vtype": os.path.join(LuST_dir, "scenario/vtypes.add.xml"),
        # features associated with the routes vehicles take
        "rou": [os.path.join(LuST_dir, "scenario/DUARoutes/local.0.rou.xml"),
                os.path.join(LuST_dir, "scenario/DUARoutes/local.1.rou.xml"),
                os.path.join(LuST_dir, "scenario/DUARoutes/local.2.rou.xml")]
    },
    additional_params=ADDITIONAL_NET_PARAMS,

)

# we no longer need to specify anything in VehicleParams
vehicles = VehicleParams()


network = Network(
    name="template",
    net_params=net_params,
    vehicles=vehicles,
)

# create the environment
env = TestEnv(
    env_params=env_params,
    sim_params=sim_params,
    network=network
)

# run the simulation for 1000 steps
exp = Experiment(env=env)
_ = exp.run(1, 1000)

