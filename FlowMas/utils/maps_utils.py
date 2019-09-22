import os
import random
from math import floor
from xml.etree import ElementTree
from xml.etree.ElementTree import XMLParser

from FlowMas.utils.parameters import Params



def get_edges(map_name, perc=1.0):
    """
    Return a list of the map edges
    :param map_name:  map name
    :param perc: (float range 0,1) the percentage of the edges to return, if !=1, then 1-perc random elements will be discarded
    :return: list
    """


    def import_edges_from_path(map_path):
        """
        Get list of edges ids from path
        :param map_path: (str) the path for the xml file
        :return: list of edges
        """
        # import the .net.xml file containing all edge/type data
        parser = XMLParser()
        tree = ElementTree.parse(map_path, parser=parser)
        root = tree.getroot()

        edges = list()

        # collect all information on the edges
        for edge in root.findall('edge'):
            edge_id=edge.attrib['id']
            if edge_id[0] != ':':
                edges.append(edge_id)

        return edges

    if map_name == 'lust':
        path = os.path.join(Params.MAP_DIRS["lust"], "scenario/lust.net.xml")
        edges = import_edges_from_path(path)

    elif map_name == 'rome':
        path = os.path.join(Params.MAP_DIRS["rome"], "rome.net.xml")
        edges = import_edges_from_path(path)


    else:
        raise NotImplementedError(f"Edge extractor for {map_name} has not been implemented yet")

    if perc != 1:
        # discarding random edges
        random.shuffle(edges)
        to_discard = floor(len(edges) * (1 - perc))
        for _ in range(to_discard):
            edges.pop()
    return edges




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
            template.update({"net": os.path.join(Params.MAP_DIRS["lust"], "scenario/lust.net.xml")})
        if vtype:
            template.update({"vtype": os.path.join(Params.MAP_DIRS["lust"], "scenario/vtypes.add.xml")})
        if rou:
            template.update({
                "rou": [os.path.join(Params.MAP_DIRS["lust"], "scenario/DUARoutes/local.0.rou.xml"),
                        os.path.join(Params.MAP_DIRS["lust"], "scenario/DUARoutes/local.1.rou.xml"),
                        os.path.join(Params.MAP_DIRS["lust"], "scenario/DUARoutes/local.2.rou.xml")]
            })

    elif "monaco" in map_name.lower():  # fixme

        if net:
            template.update({"net": os.path.join(Params.MAP_DIRS["monaco"], "scenario/in/most.net.xml")})
        if vtype:
            template.update({"vtype": os.path.join(Params.MAP_DIRS["monaco"], "/scenario/in/add/basic.vType.xml")})
        if rou:
            template.update({
                "rou": [os.path.join(Params.MAP_DIRS["monaco"], "scenario/in/route/most.buses.flows.xml"),
                        os.path.join(Params.MAP_DIRS["monaco"], "scenario/in/route/most.commercial.rou.xml"),
                        os.path.join(Params.MAP_DIRS["monaco"], "scenario/in/route/most.highway.flows.xml"),
                        os.path.join(Params.MAP_DIRS["monaco"], "scenario/in/route/most.pedestrian.rou.xml"),
                        os.path.join(Params.MAP_DIRS["monaco"], "scenario/in/route/most.special.rou.xml"),
                        os.path.join(Params.MAP_DIRS["monaco"], "scenario/in/route/most.trains.flows.xml"), ]
            })

    return template
