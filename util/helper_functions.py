from util import constants

from architecture.node import EndSystem, Switch

import networkx as nx

from itertools import islice

def convert_explicit_path_to_edge_list(explicit_path_raw, graph):
    edge_list = list()
    path = list(zip(explicit_path_raw, explicit_path_raw[1:]))
    for edge in path:
        edge_list.append(graph.get_edge(edge[0], edge[1]))

    return edge_list


def convert_explicit_path_raw_to_edge(explicit_path_raw, graph):
    path = [[explicit_path_raw[i], explicit_path_raw[i + 1]] for i in range(len(explicit_path_raw) - 1)]
    edge_list = list()
    for edge in path:
        edge_list.append(graph.get_edge(edge[0], edge[1]))
    return edge_list


def compute_mbps(message_size, cmi):
    return (message_size * constants.ONE_BYTE) / cmi

def convert_graph_to_networkx_graph(graph, source, target):
    g = nx.DiGraph()
    for node in graph.get_nodes():
        if isinstance(node, Switch):
            g.add_node(node.get_name())
        else:
            if node != source or node != target:
                g.add_node(node.get_name())

    for edge in graph.get_edges():
        g.add_edge(edge.get_source().get_name(), edge.get_target().get_name())
        g[edge.get_source().get_name()][edge.get_target().get_name()]['weight'] = edge.get_weight()

    return g

def create_explicit_path_raw(source, switch_list, target):
    explicit_path_raw = list()
    explicit_path_raw.append(source)
    for switch in switch_list:
        explicit_path_raw.append(Switch(switch))
    explicit_path_raw.append(target)

    return explicit_path_raw

def yen_k_shortest_paths(g, source, target, k, weight=None):
    return list(islice(nx.shortest_simple_paths(g, source, target, weight=weight), k))

def create_shortest_path_info_log(routing, path_finder_method, algorithm, evaluator_name):
    return f"Solving problem using {routing}, {path_finder_method}, {algorithm}, {evaluator_name}"

def found_no_solution(solution):
    return f"Found no solution: {solution.get_cost().get_detailed_string()}"

def found_solution(solution):
    return f"Found solution: {solution.get_cost().get_detailed_string()}"

def create_empty_algorithm_info_log(routing, path_finder_method, k, meta):
    return f"Solving problem using {routing}, {path_finder_method}, {k}"