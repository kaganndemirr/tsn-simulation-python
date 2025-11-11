import networkx as nx

from itertools import islice


def dijkstra_shortest_path(g, source, target, weight):
    return nx.shortest_path(g, source, target, weight=weight, method="dijkstra")

def yen_k_shortest_paths(g, source, target, k, weight):
    return list(islice(nx.shortest_simple_paths(g, source, target, weight=weight), k))