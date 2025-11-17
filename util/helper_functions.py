import re
import os
from pathlib import Path

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

    for edge in graph.get_edge_list():
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


def generate_multicast_path_for_shortest_path(path_list):
    if len(path_list) == 1:
        return path_list[0]
    else:
        final_path = path_list[0]
        for path in path_list[1:]:
            for edge in path:
                if edge not in final_path:
                    final_path.append(edge)

        return final_path


def generate_multicast_path_for_k_shortest_path(candidate_path_list_for_all_targets):
    if len(candidate_path_list_for_all_targets) == 1:
        return candidate_path_list_for_all_targets[0]
    else:
        number_of_groups = len(candidate_path_list_for_all_targets)
        number_of_items = len(candidate_path_list_for_all_targets[0])

        final_candidate_path_list = list()

        for i in range(number_of_items):
            column_lists = [candidate_path_list_for_all_targets[g][i] for g in range(number_of_groups)]

            base = column_lists[0].copy()

            for other_list in column_lists[1:]:
                for item in other_list:
                    if item not in base:
                        base.append(item)

            final_candidate_path_list.append(base)

        return final_candidate_path_list

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

def create_result_output_path(bag):
    result_list = list()

    result_list.append("outputs")
    result_list.append("PathFindingMethod=" + bag.get_path_finding_method())
    if bag.get_algorithm() is not None:
        result_list.append("Algorithm=" + bag.get_algorithm())
    if bag.get_k() is not None:
        result_list.append("K=" + str(bag.get_k()))
    if bag.get_metaheuristic_name() is not None:
        result_list.append("MetaheuristicName=" + bag.get_metaheuristic_name())

    result_output_path = Path(*result_list)

    if not result_output_path.exists():
        result_output_path.mkdir(parents=True)

    return result_output_path

def create_scenario_output_path(bag):
    result_output_path = create_result_output_path(bag)

    scenario_output_path = os.path.join(result_output_path, bag.get_topology_name() + "_" + bag.get_scenario_name())

    scenario_output_path = Path(scenario_output_path)

    if not scenario_output_path.exists():
        scenario_output_path.mkdir(parents=True)

    return scenario_output_path

def create_tsnsched_output_path(scenario_output_path):
    tsnsched_output_path = os.path.join(scenario_output_path, "tsnsched")

    tsnsched_output_path = Path(tsnsched_output_path)

    if not tsnsched_output_path.exists():
        tsnsched_output_path.mkdir(parents=True)

    return tsnsched_output_path