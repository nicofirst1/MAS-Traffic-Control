from flow.core.params import InitialConfig, TrafficLightParams
from flow.networks.base import Network


class LuSTNetwork(Network):

    def __init__(self, name, vehicles, net_params, initial_config=InitialConfig(), traffic_lights=TrafficLightParams()):


        super().__init__(name, vehicles, net_params, initial_config, traffic_lights)
