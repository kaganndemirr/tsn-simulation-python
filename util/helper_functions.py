from util import constants

from architecture.node import EndSystem, Switch

import networkx as nx

def convert_explicit_path_raw_list_to_edge(explicit_path_raw_list, graph):
    edge_list_list = list()
    for explicit_path_raw in explicit_path_raw_list:
        path = list(zip(explicit_path_raw, explicit_path_raw[1:]))
        edge_list = list()
        for edge in path:
            edge_list.append(graph.get_edge(edge[0], edge[1]))
        edge_list_list.append(edge_list)

    return edge_list_list


def convert_explicit_path_raw_to_edge(explicit_path_raw, graph):
    path = list(zip(explicit_path_raw, explicit_path_raw[1:]))
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
    explicit_path_raw.append(EndSystem(source))
    for switch in switch_list:
        explicit_path_raw.append(Switch(switch))
    explicit_path_raw.append(EndSystem(target))


    return explicit_path_raw

def create_path_raw(string_node_list):
    path_raw = list()
    for node in string_node_list:
        if isinstance(node, EndSystem):
            path_raw.append(EndSystem(node))
        elif isinstance(node, Switch):
            path_raw.append(Switch(node))

    return path_raw