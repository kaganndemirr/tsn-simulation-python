from edge import Edge

class Graph:
    def __init__(self):
        self.nodes = set()
        self.edges = set()

    def add_node(self, node):
        self.nodes.add(node)

    def add_edge(self, source_name: str, target_name: str, weight: float = 1.0):
        source = self.get_node(source_name)
        target = self.get_node(target_name)
        if source and target:
            edge = Edge(source, target, weight)
            self.edges.add(edge)

    def add_edge_direct(self, edge):
        self.edges.add(edge)

    def get_node(self, name):
        for node in self.nodes:
            if node.get_name() == name:
                return node
        return None

    def get_nodes(self):
        return self.nodes

    def get_edges(self):
        return self.edges