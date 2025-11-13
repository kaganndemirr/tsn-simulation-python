class GCL:
    def __init__(self, start, end, cycle_duration):
        self.start = start
        self.end = end
        self.cycle_duration = cycle_duration

    def get_start(self):
        return self.start

    def get_end(self):
        return self.end

    def get_duration(self):
        return self.end - self.start

    def get_cycle_duration(self):
        return self.cycle_duration

    def __repr__(self):
        return f"{self.start} - {self.end}, {self.cycle_duration}"

    def __eq__(self, other):
        if isinstance(other, GCL):
            return self.start == other.start and self.end == other.end and self.cycle_duration == other.cycle_duration
        return False

    def __hash__(self):
        return hash(self.start) + hash(self.end) + hash(self.cycle_duration)