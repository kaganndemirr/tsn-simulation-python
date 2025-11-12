import re
import os

import networkx as nx

from architecture.node import EndSystem, Switch
from util import constants


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


def generate_multicast_if_necessary_for_shortest_path(message_list):
    for message in message_list:
        merged_path = list(message.get_path_list()[0])
        if len(message.get_path_list()) > 1:
            for path in  message.get_path_list()[1:]:
                for edge in path:
                    if edge not in merged_path:
                        merged_path.append(edge)

            message.set_path_list([merged_path])

def get_topology_and_scenario_name(topology_file, scenario_file):
    topology_name = None
    scenario_name = None

    pattern_topology = re.compile(r"(.+?)(?=\.graphml)")
    matcher_topology = pattern_topology.search(os.path.basename(topology_file))
    if matcher_topology:
        topology_name = matcher_topology.group(1)

    pattern_scenario = re.compile(r"(?<=_)(.*?)(?=\.xml)")
    matcher_scenario = pattern_scenario.search(os.path.basename(scenario_file))
    if matcher_scenario:
        scenario_name = matcher_scenario.group(1)

    return topology_name, scenario_name