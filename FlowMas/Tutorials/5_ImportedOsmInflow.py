from copy import deepcopy

from FlowMas.utils.maps_utils import inflow_random_edges
# the Experiment class is used for running simulations
from FlowMas.utils.parameters import Params
from flow.controllers import IDMController
from flow.controllers.routing_controllers import MinicityRouter
from flow.core.experiment import Experiment
from flow.core.params import EnvParams, InitialConfig
from flow.core.params import NetParams
from flow.core.params import SumoParams
# all other imports are standard
from flow.core.params import VehicleParams
# the base network class
from flow.envs import TestEnv
from flow.networks import Network
from flow.networks.traffic_light_grid import ADDITIONAL_NET_PARAMS

try:
    from ray.rllib.agents.agent import get_agent_class
except ImportError:
    from ray.rllib.agents.registry import get_agent_class
from flow.core.params import InFlows

# Remove traffic lights
additional_net_params = deepcopy(ADDITIONAL_NET_PARAMS)

# Adding human vehicles
vehicles = VehicleParams()
human_num = 300
# add human drivers with premade controllers/routers
vehicles.add("human",
             acceleration_controller=(IDMController, {}),
             routing_controller=(MinicityRouter, {}),
             num_vehicles=human_num)

horizon = 1000
sim_step = 0.3
# total simulation time is horizon/sim_step seconds

# create some default parameters parameters
env_params = EnvParams(
    # length of one rollout
    horizon=horizon,

)

# the simulation parameters
sim_params = SumoParams(
    sim_step=sim_step,
    render=True,
    show_radius=True,  # show a circle on top of RL agents
    overtake_right=True,  # overtake on right to simulate more aggressive behavior
    emission_path=Params.DATA_DIR,
    restart_instance=False,
)

# setting initial configuration files
initial_config = InitialConfig(
    shuffle=True,
)

# Adding inflows
inflow = InFlows()

human_inflow = dict(
    veh_type="human",
    probability=0.001,
    depart_lane="random",
    depart_speed="random",
    begin=5,  # time in seconds to start the inflow
)

# adding human inflows
inflow_random_edges(inflow, **human_inflow)

# specify net params
net_params = NetParams(
    additional_params=additional_net_params,
    inflows=inflow,
    osm_path=Params.MAP_DIRS_DICT["groningen"] + "/osm_bbox.osm.xml"

)

# create the network
network = Network(
    name="tutorial_inflow",
    net_params=net_params,
    vehicles=vehicles,
    initial_config=initial_config,
)

# create the environment
env = TestEnv(
    env_params=env_params,
    sim_params=sim_params,
    network=network,

)

# run the simulation for 100000 steps
exp = Experiment(env=env)
_ = exp.run(1, 100000)
