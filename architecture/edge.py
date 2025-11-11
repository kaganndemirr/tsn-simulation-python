class Edge:
    def __init__(self, source, target, rate, idle_slope, weight):
        self.source = source
        self.target = target
        self.rate = rate
        self.idle_slope = idle_slope
        self.weight = weight
        self.gcl = None

    def get_source(self):
        return self.source

    def get_target(self):
        return self.target

    def get_rate(self):
        return self.rate

    def get_idle_slope(self):
        return self.idle_slope

    def get_weight(self):
        return self.weight

    def get_gcl(self):
        return self.gcl

    def set_weight(self, new_weight):
        self.weight = new_weight

    def add_gcl(self, gcl):
        self.gcl = gcl

    def __repr__(self):
        return f"({self.source} : {self.target})"

    def __eq__(self, other):
        if isinstance(other, Edge):
            return (self.source, self.target) == (other.source, other.target)
        return False

    def __hash__(self):
        return hash(self.source) + hash(self.target)
