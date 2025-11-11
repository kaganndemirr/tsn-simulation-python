import networkx as nx

from architecture.graph import Graph
from architecture.node import EndSystem, Switch

from util import constants

from itertools import islice

def compute_mbps(message_size, cmi):
    return (message_size * constants.ONE_BYTE) / cmi

def create_path_as_list(source, switch_list, target):
    explicit_path_raw = list()

    explicit_path_raw.append(source)
    for switch in switch_list:
        explicit_path_raw.append(Switch(switch))
    explicit_path_raw.append(target)

    return explicit_path_raw

def create_path_as_edge_list(path_as_list, graph):
    edge_list = list()

    path = list(zip(path_as_list, path_as_list[1:]))
    for edge in path:
        edge_list.append(graph.get_edge(edge[0], edge[1]))

    return edge_list


def convert_graph_to_nx_graph(graph, source, target):
    g = nx.DiGraph()

    for edge in graph.get_edges():
        if isinstance(edge.get_source(), Switch) and isinstance(edge.get_target(), Switch):
            g.add_edge(edge.get_source().get_name(), edge.get_target().get_name())
            g[edge.get_source().get_name()][edge.get_target().get_name()]['weight'] = edge.get_weight()

        elif edge.get_source() == source or edge.get_target() == target:
            g.add_edge(edge.get_source().get_name(), edge.get_target().get_name())
            g[edge.get_source().get_name()][edge.get_target().get_name()]['weight'] = edge.get_weight()

    return g


def create_path_as_node_list(source, switch_list, target):
    path_as_node_list = list()

    path_as_node_list.append(EndSystem(source))
    for switch in switch_list:
        path_as_node_list.append(Switch(switch))
    path_as_node_list.append(EndSystem(target))

    return path_as_node_list

def convert_explicit_path_raw_to_edge(explicit_path_raw, graph):
    path = [[explicit_path_raw[i], explicit_path_raw[i + 1]] for i in range(len(explicit_path_raw) - 1)]
    edge_list = list()
    for edge in path:
        edge_list.append(graph.get_edge(edge[0], edge[1]))
    return edge_list
