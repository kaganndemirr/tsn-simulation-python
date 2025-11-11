class GCE:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

    def get_duration(self):
        return self.end - self.start

    def __repr__(self):
        return f"[{self.start} - {self.end}]"

    def __eq__(self, other):
        if isinstance(other, GCE):
            return self.start == other.start and self.end == other.end
        return False

    def __hash__(self):
        return hash(self.start) + hash(self.end)