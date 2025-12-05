class Edge:
    def __init__(self, source, target, rate, srt_idle_slope, weight):
        self.source = source
        self.target = target
        self.rate = rate
        self.srt_idle_slope = srt_idle_slope
        self.weight = weight
        self.gcl = None

    def __repr__(self):
        return f"({self.source} : {self.target})"

    def __eq__(self, other):
        if isinstance(other, Edge):
            return (self.source, self.target) == (other.source, other.target)
        return False

    def __hash__(self):
        return hash(self.source) + hash(self.target)
