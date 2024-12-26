import xml.etree.ElementTree as Et

from util import constants

from architecture.graph import Graph
from architecture.node import Switch, EndSystem

def parse(net_file, rate, idle_slope):

    graph = Graph()

    tree = Et.parse(net_file)
    root = tree.getroot()

    for node in root.findall('node'):
        node_name = node.get('name')
        node_type = node.get('type')
        if node_type == constants.SWITCH:
            graph.add_node(Switch(node_name))
        elif node_type == constants.END_SYSTEM:
            graph.add_node(EndSystem(node_name))

    for edge in root.findall('edge'):
        source = edge.get('source')
        target = edge.get('target')
        weight = edge.get('weight')
        graph.add_edge(source, target, rate, idle_slope, weight)

    return graph