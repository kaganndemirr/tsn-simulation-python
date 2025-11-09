from architecture.edge import Edge

class Graph:
    def __init__(self):
        self.nodes = list()
        self.edges = list()

    def add_node(self, node):
        self.nodes.append(node)

    def add_edge(self, source_name, target_name, rate, idle_slope, weight,):
        source = self.get_node(source_name)
        target = self.get_node(target_name)
        if source and target:
            edge = Edge(source, target, rate, idle_slope, weight)
            self.edges.append(edge)

    def get_node(self, name):
        for node in self.nodes:
            if node.get_name() == name:
                return node
        return None

    def get_edge(self, source_node, target_node):
        for edge in self.edges:
            if edge.get_source() == source_node and edge.get_target() == target_node:
                return edge

        return None

    def get_nodes(self):
        return self.nodes

    def get_edges(self):
        return self.edges