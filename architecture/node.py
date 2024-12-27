class Node:
    def __init__(self, name):
        self.name = name

    def get_name(self):
        return self.name

    def __repr__(self):
        return f"Name: {self.name}"

    def __eq__(self, other):
        if isinstance(other, Node):
            return self.name == other.name
        return False

    def __hash__(self):
        return id(self.name)

class Switch(Node):
    def __init__(self, name):
        super().__init__(name)

class EndSystem(Node):
    def __init__(self, name):
        super().__init__(name)