from architecture.edge import Edge
from architecture.node import EndSystem, Switch


class Graph:
    def __init__(self):
        self.node_list = list()
        self.edge_list = list()

    def add_node(self, node):
        self.node_list.append(node)

    def add_edge(self, source, target, rate, idle_slope, weight):
        edge = Edge(source, target, rate, idle_slope, weight)
        self.edge_list.append(edge)

    def get_node(self, name):
        for node in self.node_list:
            if node.get_name() == name:
                return node
        return None

    def get_edge(self, source_node, target_node):
        for edge in self.edge_list:
            if edge.get_source() == source_node and edge.get_target() == target_node:
                return edge

        return None

    def get_node_list(self):
        return self.node_list

    def get_edge_list(self):
        return self.edge_list

    def get_switch_list(self):
        switch_list = list()
        for node in self.node_list:
            if isinstance(node, Switch):
                switch_list.append(node)
        return switch_list

    def get_end_system_list(self):
        switch_list = list()
        for node in self.node_list:
            if isinstance(node, EndSystem):
                switch_list.append(node)
        return switch_list