import xml.etree.ElementTree as Et

from util import constants

from architecture.graph import Graph
from architecture.node import Switch, EndSystem

def tsncf_topology_parser(net_file, rate, idle_slope):

    graph = Graph()

    tree = Et.parse(net_file)
    root = tree.getroot()

    namespace = {'graphml': 'http://graphml.graphdrawing.org/xmlns'}

    graph_element = root.find("graphml:graph", namespace)
    edge_type = graph_element.attrib.get('edgedefault')

    for node in root.findall('.//graphml:node', namespace):
        node_name = node.get('id')
        data_element = node.find('graphml:data', namespace)
        if data_element is not None:
            data_value = data_element.text
            if data_value == constants.SWITCH:
                graph.add_node(Switch(node_name))
            elif data_value == constants.END_SYSTEM:
                graph.add_node(EndSystem(node_name))

    for edge in root.findall('.//graphml:edge', namespace):
        source_element = edge.attrib['source']
        target_element = edge.attrib['target']
        graph.add_edge(source_element, target_element, rate, idle_slope)
        if edge_type == constants.UNDIRECTED:
            source_element = edge.attrib['target']
            target_element = edge.attrib['source']
            graph.add_edge(source_element, target_element, rate, idle_slope)

    return graph


def tsnrot_topology_parser(net_file, idle_slope):

    graph = Graph()

    tree = Et.parse(net_file)
    root = tree.getroot()

    namespace = {'graphml': 'http://graphml.graphdrawing.org/xmlns'}

    for node in root.findall('.//graphml:node', namespace):
        node_name = node.get('id')
        data_element = node.find('graphml:data', namespace)
        if data_element is not None:
            data_value = data_element.text
            if data_value == constants.SWITCH:
                graph.add_node(Switch(node_name))
            elif data_value == constants.END_SYSTEM:
                graph.add_node(EndSystem(node_name))

    # TODO: Not Completed
    for edge in root.findall('.//graphml:edge', namespace):
        source_element = edge.attrib['source']
        target_element = edge.attrib['target']
        data_element = edge.findall('graphml:data', namespace)
        if data_element is not None:
            graph.add_edge(source_element, target_element, 0, idle_slope)

    return graph