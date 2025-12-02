class Node:
    def __init__(self, name):
        self.name = name
        self.port_list = list()

    def add_port(self, port):
        self.port_list.append(port)

    def get_port_list(self):
        return self.port_list

    def __repr__(self):
        return f"{self.name}"

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.name == other.name
        return False

    def __hash__(self):
        return hash(self.name)

class Switch(Node):
    def __init__(self, name):
        super().__init__(name)

class EndSystem(Node):
    def __init__(self, name):
        super().__init__(name)

class Port:
    def __init__(self, name, connects_to):
        self.name = name
        self.connects_to = connects_to

    def get_name(self):
        return self.name

    def get_connects_to(self):
        return self.connects_to