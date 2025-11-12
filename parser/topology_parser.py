import xml.etree.ElementTree as Et

from util import constants

from architecture.graph import Graph
from architecture.node import Switch, EndSystem, Port

def topology_parser(net_file):

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

    node_port_id_dict = dict()
    for edge in root.findall('.//graphml:edge', namespace):
        source_element = edge.attrib['source']
        target_element = edge.attrib['target']
        
        rate = None
        edge_type = None
        idle_slope = None
        weight = 1.0
        
        for data in edge.findall('graphml:data', namespace):
            key = data.get('key')
            if key == 'd1':
                rate = int(data.text) if data.text else None
            elif key == 'd2':
                edge_type = data.text if data.text else None
            elif key == 'd3':
                idle_slope = float(data.text) if data.text else None
            elif key == 'd4':
                weight = float(data.text) if data.text else 1.0

        source = graph.get_node(source_element)
        target = graph.get_node(target_element)

        graph.add_edge(source, target, rate, idle_slope, weight)

        if source not in node_port_id_dict.keys():
            node_port_id_dict[source] = 0
        else:
            node_port_id_dict[source] += 1

        port = Port("eth" + str(node_port_id_dict[source]), target.get_name())
        source.add_port(port)
        if edge_type == constants.UNDIRECTED:
            graph.add_edge(target, source, rate, idle_slope, weight)

            if target not in node_port_id_dict.keys():
                node_port_id_dict[target] = 0
            else:
                node_port_id_dict[target] += 1

            port = Port("eth" + str(node_port_id_dict[target]), source.get_name())
            target.add_port(port)

    return graph