from util import constants

from architecture.node import Switch

import networkx as nx

def convert_to_edge(path_raw, graph):
    path = list(zip(path_raw, path_raw[1:]))
    edge_list = list()
    for edge in path:
        edge_list.append(graph.get_edge(edge[0], edge[1]))
    return edge_list


def compute_mbps(message_size, cmi):
    return (message_size * constants.ONE_BYTE) / cmi

def convert_graph_to_nx_graph(graph):
    g = nx.DiGraph()
    for node in graph.get_nodes():
        g.add_node(node.get_name())

    for edge in graph.get_edges():
        g.add_edge(edge.get_source().get_name(), edge.get_target().get_name())
        g[edge.get_source().get_name()][edge.get_target().get_name()]['weight'] = edge.get_weight()

    return g

def create_explicit_path_raw(source, switch_list, target):
    explicit_path_raw = list()
    explicit_path_raw.append(source)
    for switch in switch_list:
        explicit_path_raw.append(Switch(switch.get('name')))
    explicit_path_raw.append(target)

    return explicit_path_raw

def create_path_raw(string_switch_list):
    path_raw = list()
    for switch in string_switch_list:
        path_raw.append(Switch(switch))

    return path_raw