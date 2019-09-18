import os

MAP_DIRS = dict(

    lust=os.path.join(os.getcwd().split("FlowMas")[0], "FlowMas/maps/LuSTScenario"),
    monaco=os.path.join(os.getcwd().split("FlowMas")[0], "FlowMas/maps/MoSTScenario"),
)


def import_map(map_name, net=True, vtype=False, rou=False):
    """
    Import a map from the map dir, it can be imported using various features
    :param map_name: (string) the name of the map
    :param net: (bool) network geometry features
    :param vtype: (bool) The vehicle types file describing the
    properties of different vehicle types in the network. These include parameters such as the max acceleration and
    comfortable deceleration of drivers.
    :param rou: (bool)  These files help define which cars enter the network at which point in time,
    whether it be at the beginning of a simulation or some time during it run
    :return: (dict) return the template which can be then used into the NetParams function
    """

    template = {}

    if "lust" in map_name.lower():

        if net:
            template.update({"net": os.path.join(MAP_DIRS["lust"], "scenario/lust.net.xml")})
        if vtype:
            template.update({"vtype": os.path.join(MAP_DIRS["lust"], "scenario/vtypes.add.xml")})
        if rou:
            template.update({
                "rou": [os.path.join(MAP_DIRS["lust"], "scenario/DUARoutes/local.0.rou.xml"),
                        os.path.join(MAP_DIRS["lust"], "scenario/DUARoutes/local.1.rou.xml"),
                        os.path.join(MAP_DIRS["lust"], "scenario/DUARoutes/local.2.rou.xml")]
            })

    elif "monaco" in map_name.lower():

        if net:
            template.update({"net": os.path.join(MAP_DIRS["monaco"], "scenario/in/most.net.xml")})
        if vtype:
            template.update({"vtype": os.path.join(MAP_DIRS["monaco"], "/scenario/in/add/basic.vType.xml")})
        if rou:
            template.update({
                "rou": [os.path.join(MAP_DIRS["monaco"], "scenario/in/route/most.buses.flows.xml"),
                        os.path.join(MAP_DIRS["monaco"], "scenario/in/route/most.commercial.rou.xml"),
                        os.path.join(MAP_DIRS["monaco"], "scenario/in/route/most.highway.flows.xml"),
                        os.path.join(MAP_DIRS["monaco"], "scenario/in/route/most.pedestrian.rou.xml"),
                        os.path.join(MAP_DIRS["monaco"], "scenario/in/route/most.special.rou.xml"),
                        os.path.join(MAP_DIRS["monaco"], "scenario/in/route/most.trains.flows.xml"), ]
            })

    return template
